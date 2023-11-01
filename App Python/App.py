import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFrame, QVBoxLayout, QMenu, QAction, QToolButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

class CustomToolButton(QToolButton):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self)

    def sizeHint(self):
        size_hint = super().sizeHint()
        size_hint.setHeight(size_hint.height() // 2)  # Halve the height
        return size_hint

class MovableImageWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.setWindowTitle("Movable Image Window")
        self.setGeometry(100, 100, 120, 140)  # Increased width and height

        central_widget = QFrame(self)
        self.setCentralWidget(central_widget)

        # Set a fixed background color (RGB: 31, 45, 90)
        central_widget.setStyleSheet("background-color: rgb(31, 45, 90);")

        image_path = 'logos/png/logo-only-color.png'
        original_pixmap = QPixmap(image_path)
        scaled_pixmap = original_pixmap.scaled(100, 100, Qt.KeepAspectRatio)

        image_label = QLabel(central_widget)
        image_label.setPixmap(scaled_pixmap)

        main_layout = QVBoxLayout()  # Use a vertical layout
        main_layout.addWidget(image_label)

        # Create a button for the dropdown menu
        self.icon_button = CustomToolButton()
        self.icon_button.setIcon(QIcon('Settings.png'))
        self.icon_button.setPopupMode(QToolButton.InstantPopup)
        self.icon_button.setStyleSheet("background-color: #2F76DB;")  # Set the button background color to hex #2F76DB

        # Create a dropdown menu with icons and set the width
        self.icon_menu = QMenu(self)
        self.icon_menu.aboutToShow.connect(self.adjustMenuWidth)  # Adjust the menu width before showing
        icon_names = ['Camera.png', 'Map.png', 'Phone.png', 'Settings.png', 'Weather.png', 'Calendar.png', 'Clock.png', 'Mail.png', 'Notes.png', 'Photos.png']

        # Add actions for opening applications
        app_paths = {
            'Camera': 'start microsoft.windows.camera:',  # Windows 11 Camera app command
            'Map': 'start microsoft-edge:http://maps.google.com',  # Open Google Maps in the default web browser
            'Phone': 'start microsoft-edge:http://meet.google.com',  # Open Google Meet in the default web browser
            'Settings': 'start ms-settings:',  # Windows 10/11 Settings app command
            'Weather': 'start ms-weather:',  # Windows 11 Weather app command
            'Calendar': 'start microsoft-edge:https://calendar.google.com', # Windows 11 Calendar app command
            'Clock': 'start ms-clock:', # Windows 11 Clock app command
            'Mail': 'start ms-mail:', # Windows 11 Mail app command
            'Notes': 'start ms-notepad:', # Windows 11 Notepad app command
            'Photos': 'start ms-photos:' # Windows 11 Photos app command
        }
        for icon_name in icon_names:
            action = QAction(QIcon(f'icons/{icon_name}'), icon_name.split('.')[0], self)
            if icon_name.split('.')[0] in app_paths:
                action.triggered.connect(lambda checked, app=icon_name.split('.')[0]: self.openApplication(app, app_paths[app]))
            self.icon_menu.addAction(action)

        self.icon_button.setMenu(self.icon_menu)

        main_layout.addWidget(self.icon_button)  # Add the button to the layout

        # Set the width of the button to 100
        self.icon_button.setFixedWidth(100)

        central_widget.setLayout(main_layout)

        central_widget.setMouseTracking(True)
        central_widget.mousePressEvent = self.mousePressEvent
        central_widget.mouseMoveEvent = self.mouseMoveEvent

    def adjustMenuWidth(self):
        menu_size = self.icon_button.sizeHint()
        self.icon_menu.setFixedWidth(100)

    def openApplication(self, app_name, app_command):
        try:
            subprocess.Popen(app_command, shell=True)
        except Exception as e:
            print(f"Error opening {app_name}: {str(e)}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
        elif event.button() == Qt.RightButton:
            self.showContextMenu(event.globalPos())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            new_pos = event.globalPos() - self.offset
            self.move(new_pos)

    def showContextMenu(self, pos):
        context_menu = QMenu(self)

        close_action = QAction(QIcon('close.png'), "Close", self)
        close_action.triggered.connect(self.close)

        context_menu.addAction(close_action)
        context_menu.exec_(pos)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovableImageWindow()
    window.show()
    sys.exit(app.exec_())
