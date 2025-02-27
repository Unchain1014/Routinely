import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QWidget, QDialog, QFileDialog, QFrame, QSizePolicy
from PyQt6 import uic
from PyQt6.QtCore import Qt, QSize
from utils.unsaved_prompt import UnsavedChangesDialog
from utils.serialization import save_routine_to_file

class TaskItem(QWidget):
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
        for i in range(self.parent_list.count()):
            item = self.parent_list.item(i)
            if self.parent_list.itemWidget(item) is self:
                self.parent_list.takeItem(i)

                if i == 0 and self.parent_list.count() > 0: # Remove divider below this task if this task is first
                    self.parent_list.takeItem(i)
                elif i > 0: # Remove divider above this task
                    self.parent_list.takeItem(i - 1)

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
        if not self.current_file_path:
            self.save_routine_as()
            if not self.current_file_path: # If still none, user canceled
                print("Save canceled")
                return

        success = save_routine_to_file(self.current_file_path, self.taskList)
        if success:
            print(f"Routine saving complete")
        else:
            print("Save failed")

    def save_routine_as(self):        
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
        task_text = self.newTextField.text().strip()
        selected_time = self.timeEdit.text()
        notify = self.notifyCheckBox.isChecked()
        repeat = self.repeatCheckBox.isChecked()

        if task_text:
            # Add a line separator (except for the last task)
            if self.taskList.count() > 0:
                line_item = QListWidgetItem(self.taskList)
                line_frame = QFrame()
                line_frame.setFrameShape(QFrame.Shape.HLine)
                line_frame.setFrameShadow(QFrame.Shadow.Sunken)
                line_frame.setStyleSheet("color: gray;")
                line_frame.setFixedHeight(2)
                line_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                self.taskList.setItemWidget(line_item, line_frame)
                line_item.setSizeHint(QSize(0, 2))  # (width, height)
                line_item.setFlags(Qt.ItemFlag.NoItemFlags)
                self.taskList.updateGeometry()

            # Create a QListWidgetItem for the task
            item = QListWidgetItem(self.taskList)
            task_widget = TaskItem(selected_time, task_text, notify, repeat, self.taskList, self)
            self.taskList.setItemWidget(item, task_widget)
            item.setSizeHint(task_widget.sizeHint())

            # Clear input field
            self.newTextField.clear()

    def clear_tasks(self):
        if self.taskList:
            self.taskList.clear()

    def quit_triggered(self):
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConverterWindow()
    window.show()
    sys.exit(app.exec())