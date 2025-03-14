from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl

class AudioManager:
    def __init__(self):
        self.sound = QSoundEffect()
        self.sound.setSource(QUrl.fromLocalFile("src/sounds/notification.wav"))  # Adjust path if needed
        self.sound.setLoopCount(1)  # Default to playing once

    def play_notification_sound(self, loop=False):
        self.sound.setLoopCount(-1 if loop else 1)  # Use -1 for infinite looping
        self.sound.play()

    def stop_notification_sound(self):
        self.sound.stop()