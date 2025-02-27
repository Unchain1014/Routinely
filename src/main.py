import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QWidget, QDialog, QFileDialog
from PyQt6 import uic
from PyQt6.QtCore import Qt
from utils.unsaved_prompt import UnsavedChangesDialog
from utils.serialization import save_routine_to_file

class TaskItem(QWidget):
    """Custom task widget."""
    def __init__(self, time, text, notify, repeat, parent_list, parent_window):
        super().__init__()

        # Load the task item UI
        uic.loadUi("src/ui/task_item.ui", self)

        self.parent_list = parent_list
        self.parent_window = parent_window

        # Store notify and repeat states as attributes
        self.notify = notify
        self.repeat = repeat

        # Set checkbox text with time prefix
        self.checkBox.setText(f"{time} - {text}")

        # Connect delete button to remove item
        self.deleteButton.clicked.connect(self.delete_task)

    def delete_task(self):
        """Remove task item from list."""
        for i in range(self.parent_list.count()):
            item = self.parent_list.item(i)
            if self.parent_list.itemWidget(item) is self:
                self.parent_list.takeItem(i)
                break # Stop after removing the first match

class ConverterWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI file
        uic.loadUi("src/ui/design.ui", self)

        # Track last saved file path
        self.current_file_path = None

        # Connect button click to add task method
        self.addTaskButton.clicked.connect(self.add_task)

        # Connect Enter key press in newTextField to add task
        self.newTextField.returnPressed.connect(self.add_task)

        # Connect Clear Routine button to remove all tasks
        self.clearRoutineButton.clicked.connect(self.clear_tasks)

        # Connect Save menubar action
        self.actionSave.triggered.connect(self.save_routine)

        # Connect Save As menubar action
        self.actionSave_As.triggered.connect (self.save_routine_as)

        # Connect Load Routine menubar action
        self.actionLoad_Routine.triggered.connect(self.on_load_routine_triggered)
        
        # Connect Quit menubar action
        self.actionQuit.triggered.connect(self.quit_triggered)

    # When load routine is triggered, call this method first
    def on_load_routine_triggered(self):
        if self.has_unsaved_changes(): # NOT YET IMPLEMENTED
            self.handle_unsaved_changes()
        else:
            self.load_routine()

    def has_unsaved_changes(self):
        return True # Replace with actual logic later

    def handle_unsaved_changes(self):
        dialog = UnsavedChangesDialog(self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            self.save_routine()
            self.load_routine()
        elif result == QDialog.DialogCode.Rejected:
            self.load_routine()
        # If canceled, do nothing

    # Load routine is not to be called directly, or unsaved changes check will be missed
    def load_routine(self):
        print("Load routine logic here.")

    def save_routine(self):
        """Saves the current routine to the last saved file, or asks for a location if not set."""
        if not self.current_file_path:
            return self.save_routine_as()  # If no file is selected, use Save As

        success = save_routine_to_file(self.current_file_path, self.taskList)
        if success:
            print(f"Routine saving complete")
        else:
            print("Save failed")

    def save_routine_as(self):
        """Saves the routine with a file dialog, starting in the 'routines/' subdirectory."""
        
        # Ensure the routines/ directory exists
        default_dir = os.path.join(os.getcwd(), "routines")
        os.makedirs(default_dir, exist_ok=True)  # Create if it doesn't exist

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Routine", default_dir, "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            self.current_file_path = file_path  # Store the new file path
            success = save_routine_to_file(file_path, self.taskList)
            if success:
                print(f"Routine saving complete")
            else:
                print("Save failed")

    def add_task(self):
        """Adds a new task to the task list."""
        task_text = self.newTextField.text().strip()
        selected_time = self.timeEdit.text()

        # Retrieve notify and repeat states from input fields
        notify = self.notifyCheckBox.isChecked()
        repeat = self.repeatCheckBox.isChecked()

        if task_text:
            # Create a QListWidgetItem
            item = QListWidgetItem(self.taskList)

            # Create a custom TaskItem widget
            task_widget = TaskItem(selected_time, task_text, notify, repeat, self.taskList, self)

            # Add the TaskItem widget to task list
            self.taskList.setItemWidget(item, task_widget)
            item.setSizeHint(task_widget.sizeHint())

            # Clear input field
            self.newTextField.clear()

    def clear_tasks(self):
        """Removes all tasks from the task list."""
        if self.taskList:
            self.taskList.clear()

    def quit_triggered(self):
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConverterWindow()
    window.show()
    sys.exit(app.exec())