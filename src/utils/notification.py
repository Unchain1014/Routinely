from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from utils.audio_manager import AudioManager  # <-- FIXED: Import AudioManager

class NotificationDialog(QDialog):
    """Modal notification window that forces user interaction."""
    def __init__(self, task_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task Reminder")
        self.setModal(True)  # Prevents user from interacting with the main window
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)  # Always on top
        self.setFixedSize(300, 100)  # Set a fixed size for the dialog

        # Initialize AudioManager for looping notification sound
        self.audio_manager = AudioManager()  
        self.audio_manager.play_notification_sound(loop=True)  # Play sound in a loop

        # Set up the layout
        layout = QVBoxLayout(self)

        # Task message label (centered text)
        self.message_label = QLabel(task_text, self)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center text
        layout.addWidget(self.message_label)

        # Okay button
        self.okay_button = QPushButton("Okay", self)
        self.okay_button.clicked.connect(self.stop_sound_and_close)  # Stop sound on click
        layout.addWidget(self.okay_button, alignment=Qt.AlignmentFlag.AlignCenter)  # Center button

    def stop_sound_and_close(self):
        """Stops the notification sound and closes the dialog."""
        self.audio_manager.stop_notification_sound()
        self.accept()