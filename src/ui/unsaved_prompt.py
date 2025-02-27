import os
from PyQt6.QtWidgets import QDialog, QPushButton, QDialogButtonBox
from PyQt6 import uic

class UnsavedChangesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), "unsaved_prompt_design.ui")
        uic.loadUi(ui_path, self)

        # Set standard buttons
        self.unsavedButtonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Discard | 
            QDialogButtonBox.StandardButton.Cancel
        )

        # Rename buttons
        self.unsavedButtonBox.button(QDialogButtonBox.StandardButton.Save).setText("Save and Load")
        self.unsavedButtonBox.button(QDialogButtonBox.StandardButton.Discard).setText("Discard and Load")
        self.unsavedButtonBox.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancel")

        # Preselect "Cancel"
        self.unsavedButtonBox.button(QDialogButtonBox.StandardButton.Cancel).setDefault(True)

        # Connect button actions
        self.unsavedButtonBox.accepted.connect(self.accept)
        self.unsavedButtonBox.rejected.connect(self.reject)

        # Manually connect "Discard and Load" since it uses DestructiveRole
        discard_btn = self.unsavedButtonBox.button(QDialogButtonBox.StandardButton.Discard)
        if discard_btn:
            discard_btn.clicked.connect(self.reject)  # Ensures "Discard and Load" works