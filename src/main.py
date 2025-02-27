import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QWidget, QDialog
from PyQt6 import uic  # Load UI files dynamically
from PyQt6.QtCore import Qt
from ui.unsaved_prompt import UnsavedChangesDialog

class TaskItem(QWidget):
    """Custom task widget."""
    def __init__(self, time, text, parent_list, parent_window):
        super().__init__()

        # Load the task item UI
        uic.loadUi("src/ui/task_item.ui", self)

        self.parent_list = parent_list
        self.parent_window = parent_window

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

        # Connect button click to add task method
        self.addTaskButton.clicked.connect(self.add_task)

        # Connect Enter key press in newTextField to add task
        self.newTextField.returnPressed.connect(self.add_task)

        # Connect Clear Routine button to remove all tasks
        self.clearRoutineButton.clicked.connect(self.clear_tasks)

        # Connect Save Routine menubar action
        self.actionSave.triggered.connect(self.save_routine)

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
        print("Save routine logic here.")

    def add_task(self):
        """Adds a new task to the task list."""
        task_text = self.newTextField.text().strip()
        selected_time = self.timeEdit.text()

        if task_text:
            # Create a QListWidgetItem
            item = QListWidgetItem(self.taskList)

            # Create a custom TaskItem widget
            task_widget = TaskItem(selected_time, task_text, self.taskList, self)

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