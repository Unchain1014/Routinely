import os
import json
from PyQt6.QtWidgets import QListWidgetItem, QFrame, QSizePolicy
from PyQt6.QtCore import Qt, QSize

def save_routine_to_file(file_path, task_list, task_item_class):
    # Extract routine name from file name (remove extension)
    routine_name = os.path.splitext(os.path.basename(file_path))[0]

    tasks = []
    for i in range(task_list.count()):
        item = task_list.item(i)
        task_widget = task_list.itemWidget(item)

        if not isinstance(task_widget, task_item_class):
            continue # Skip this item if not a task widget

        if task_widget:
            # Extract time and title from the checkbox text
            time, title = task_widget.checkBox.text().split(" - ", 1)

            # Remove any narrow no-break spaces from the time string
            time = time.replace("\u202f", "").strip()

            task_data = {
                "title": title,
                "time": time,
                "notify": task_widget.notify,
                "repeat": task_widget.repeat,
                "checkbox_state": task_widget.checkBox.isChecked()
            }
            tasks.append(task_data)

    routine_data = {
        "routine_name": routine_name,  # Now correctly reflects the filename
        "tasks": tasks
    }

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(routine_data, file, indent=4)
        print(f"Serialized data saved successfully to {file_path}")
        return True
    except Exception as e:
        print(f"Error saving routine: {e}")
        return False

def load_routine_from_file(file_path, task_list, task_item_class, parent_window=None):
    # Ensure the file exists before trying to open it
    if not os.path.isfile(file_path):
        print(f"Error: File not found - {file_path}")
        return False

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Extract routine name (not used in taskList, but available)
        routine_name = data.get("routine_name", "Untitled Routine")

        # Clear the current task list before loading new tasks
        task_list.clear()

        for index, task in enumerate(data.get("tasks", [])):
            title = task.get("title", "Untitled Task")
            time = task.get("time", "00:00").replace("\u202f", "").strip()
            notify = task.get("notify", False)
            repeat = task.get("repeat", False)
            checkbox_state = task.get("checkbox_state", False)

            # Create a QListWidgetItem for the task
            item = QListWidgetItem(task_list)
            task_widget = task_item_class(time, title, notify, repeat, task_list, parent_window)

            # Set the checkbox state as per the saved value
            task_widget.checkBox.setChecked(checkbox_state)

            task_list.setItemWidget(item, task_widget)
            item.setSizeHint(task_widget.sizeHint())

        print(f"Routine '{routine_name}' loaded successfully from {file_path}")
        return True

    except Exception as e:
        print(f"Error loading routine: {e}")
        return False