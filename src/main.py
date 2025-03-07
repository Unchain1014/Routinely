import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem, QWidget, QDialog, QFileDialog, QFrame, QSizePolicy, QSystemTrayIcon
from PyQt6 import uic
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize, QTimer, QDateTime
from utils.unsaved_prompt import UnsavedChangesDialog
from utils.serialization import save_routine_to_file, load_routine_from_file

class TaskItem(QWidget):
    def __init__(self, time, text, notify, repeat, parent_list, parent_window):
        super().__init__()
        uic.loadUi("src/ui/task_item.ui", self)
        self.parent_list = parent_list
        self.parent_window = parent_window
        self.notify = notify
        self.repeat = repeat
        self.checkBox.setText(f"{time} - {text}")
        self.deleteButton.clicked.connect(self.delete_task)

    def delete_task(self):
        for i in range(self.parent_list.count()):
            item = self.parent_list.item(i)
            if self.parent_list.itemWidget(item) is self:
                self.parent_list.takeItem(i)
                break

class ConverterWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("src/ui/icon.svg"))  # Replace with the path to your icon file
        self.tray_icon.show()

        # Load the UI file
        uic.loadUi("src/ui/design.ui", self)

        # Track last saved file path
        self.current_file_path = None
        self.last_saved_state = {"tasks": []}  # Empty routine by default (used for)

        # Connect actions/buttons
        self.addTaskButton.clicked.connect(self.add_task)
        self.newTextField.returnPressed.connect(self.add_task)
        self.clearRoutineButton.clicked.connect(self.clear_tasks)
        self.actionNew.triggered.connect(self.new_routine)
        self.actionSave.triggered.connect(self.save_routine)
        self.actionSave_As.triggered.connect(self.save_routine_as)
        self.actionLoad_Routine.triggered.connect(self.on_load_routine_triggered)
        self.actionQuit.triggered.connect(self.close)
        self.actionTest_Notification.triggered.connect(lambda: self.show_notification("Test Notification"))

        # Initialize timer
        self.notification_timer = QTimer(self)
        self.notification_timer.timeout.connect(self.check_notifications)
        self.notification_timer.start(60_000) # Check every 60 seconds

    def check_notifications(self):
        current_time = QTime.currentTime().toString("HH:mm")  # 24-hour format

        for i in range(self.taskList.count()):
            item = self.taskList.item(i)
            task_widget = self.taskList.itemWidget(item)

            if isinstance(task_widget, TaskItem) and task_widget.notify:
                task_time = task_widget.checkBox.text().split(" - ")[0]

                if task_time == current_time:
                    self.show_notification(task_widget.checkBox.text())

                    if not task_widget.repeat:
                        self.taskList.takeItem(i)  # Remove task if repeat=False

    def show_notification(self, task_text):
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon.show()
            self.tray_icon.showMessage(
                "Routinely | Task Reminder",
                task_text,
                QSystemTrayIcon.MessageIcon.Information,
                999999  # Duration in milliseconds
            )
        else: # Fallback to QMessageBox if system tray is not available
            notification = QMessageBox(self)
            notification.setWindowTitle("Routinely | Task Reminder")
            notification.setText(f"{task_text}")
            notification.setIcon(QMessageBox.Icon.Information)
            notification.setStandardButtons(QMessageBox.StandardButton.Ok)
            notification.exec()

    def new_routine(self):
        if self.has_unsaved_changes():
            dialog = UnsavedChangesDialog(self)
            result = dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                self.save_routine()
            elif result == QDialog.DialogCode.Rejected:
                pass  # Continue with creating a new routine
            else:
                return  # User canceled, don't create a new routine

        self.clear_tasks()
        self.current_file_path = None
        self.last_saved_state = {"tasks": []}
        print("New routine created")

    def on_load_routine_triggered(self):
        if self.has_unsaved_changes():
            self.handle_unsaved_changes()
        else:
            self.load_routine()

    def has_unsaved_changes(self):
        if self.current_file_path is None and not self.get_routine_state():
            # If no file is loaded and the routine is empty, assume no unsaved changes
            return False

        current_state = self.get_routine_state()

        # If a file is loaded, but no changes have been made yet, the routine is not marked as unsaved
        if self.current_file_path and current_state == self.last_saved_state:
            return False  # No unsaved changes if current state matches last saved state

        # If current state differs from the last saved state, it means there are unsaved changes
        return current_state != self.last_saved_state

    def handle_unsaved_changes(self):
        dialog = UnsavedChangesDialog(self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            self.save_routine()
            self.load_routine()
        elif result == QDialog.DialogCode.Rejected:
            self.load_routine()
        # If canceled, do nothing

    def load_routine(self):
        default_dir = os.path.join(os.getcwd(), "routines")  # Open file dialog in the 'routines/' directory
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Routine", default_dir, "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            success = load_routine_from_file(file_path, self.taskList, TaskItem, self)
            if success:
                self.current_file_path = file_path  # Track the loaded file
                self.last_saved_state = self.get_routine_state()
                print(f"Loaded routine from {file_path}")
            else:
                print("Failed to load routine")

    def save_routine(self):
        if not self.current_file_path:
            self.save_routine_as()
            if not self.current_file_path:  # If still None, user canceled
                print("Save canceled")
                return

        success = save_routine_to_file(self.current_file_path, self.taskList, TaskItem)
        if success:
            self.last_saved_state = self.get_routine_state()  # Save the current state
            print(f"Routine saving complete")
        else:
            print("Save failed")

    def save_routine_as(self):        
        default_dir = os.path.join(os.getcwd(), "routines") # Ensure the routines/ directory exists
        os.makedirs(default_dir, exist_ok=True)  # Create if it doesn't exist

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Routine", default_dir, "JSON Files (*.json);;All Files (*)"
        )

        if file_path and not file_path.lower().endswith(".json"):
            file_path += ".json"

        if file_path:
            self.current_file_path = file_path  # Store the new file path
            success = save_routine_to_file(file_path, self.taskList, TaskItem)
            if success:
                print(f"Routine saving complete")
            else:
                print("Save failed")

    def get_routine_state(self):
        tasks = []
        for i in range(self.taskList.count()):
            item = self.taskList.item(i)
            task_widget = self.taskList.itemWidget(item)

            if isinstance(task_widget, TaskItem):
                time_str, title = task_widget.checkBox.text().split(" - ", 1)
                time_obj = datetime.strptime(time_str, "%I:%M %p").time()  # Convert time to datetime.time object

                tasks.append({
                    "time": time_obj,
                    "title": title,
                    "notify": task_widget.notify,
                    "repeat": task_widget.repeat,
                    "checkbox_state": task_widget.checkBox.isChecked()
                })

        tasks.sort(key=lambda x: x["time"])  # Sort tasks by time in ascending order
        return {"tasks": tasks}

    def add_task(self):
        task_text = self.newTextField.text().strip()
        selected_time = self.timeEdit.text()
        notify = self.notifyCheckBox.isChecked()
        repeat = self.repeatCheckBox.isChecked()

        if task_text: # Create a new dictionary with the task details and the time as a datetime.time object
            new_task = {
                "time": datetime.strptime(selected_time, "%I:%M %p").time(),
                "title": task_text,
                "notify": notify,
                "repeat": repeat,
                "checkbox_state": False
            }

            current_state = self.get_routine_state() # Get the current routine state

            # Insert the new task at the correct position based on time
            tasks = current_state["tasks"]
            tasks.append(new_task)
            tasks.sort(key=lambda x: x["time"])  # Sort tasks by time in ascending order

            self.taskList.clear() # Clear the task list

            # Add the sorted tasks back to the task list
            for task in tasks:
                item = QListWidgetItem(self.taskList)
                task_widget = TaskItem(task["time"].strftime("%I:%M %p"), task["title"], task["notify"], task["repeat"], self.taskList, self)
                task_widget.checkBox.setChecked(task["checkbox_state"])
                self.taskList.setItemWidget(item, task_widget)
                item.setSizeHint(task_widget.sizeHint())

            self.newTextField.clear() # Clear input field

    def clear_tasks(self):
        if self.taskList:
            self.taskList.clear()
            
    def closeEvent(self, event):
        if self.has_unsaved_changes():
            dialog = UnsavedChangesDialog(self)
            result = dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                self.save_routine()
                event.accept()
            elif result == QDialog.DialogCode.Rejected:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConverterWindow()
    window.show()
    sys.exit(app.exec())