import json

import os
import json

def save_routine_to_file(file_path, task_list):
    """Saves the given routine and task list to a JSON file."""

    # Extract routine name from file name (remove extension)
    routine_name = os.path.splitext(os.path.basename(file_path))[0]

    tasks = []
    for i in range(task_list.count()):
        item = task_list.item(i)
        task_widget = task_list.itemWidget(item)

        if task_widget:
            # Extract time and title from the checkbox text
            time, title = task_widget.checkBox.text().split(" - ", 1)

            # Remove any narrow no-break spaces from the time string
            time = time.replace("\u202f", "").strip()

            task_data = {
                "title": title,
                "time": time,
                "notify": task_widget.notify,  # Placeholder for future implementation
                "repeat": task_widget.repeat,  # Placeholder for future implementation
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