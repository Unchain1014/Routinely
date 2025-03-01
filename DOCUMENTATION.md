# Routinely Documentation

Routinely is a lightweight, open-source daily routine tracker designed for Linux and Windows. It provides an uncluttered interface with essential features for managing tasks and routines efficiently.

## Features

- **Task Management:** Add, delete, and manage tasks with ease.
- **Multiple Routine Tabs:** Organize tasks into different routines.
- **Offline Usage:** No internet connection or account required.
- **Cross-Platform Compatibility:** Works on both Linux and Windows using PyQt6.

## Getting Started

### Prerequisites

- Python 3 (latest version recommended)
- PyQt6
- Git

### Installation

1. **Clone the Repository:**
   ```bash
   git clone git@github.com:Unchain1014/Routinely.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd Routinely
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   python src/main.py
   ```

## Usage

### Main Window

- **Clear Routine:** Click the "Clear Routine" button to remove all tasks from the current routine.
- **Save Routine:** Use the "Save" option in the menu to save the current routine to a file.
- **Load Routine:** Use the "Load Routine" option in the menu to load a routine from a file.
- **New Routine:** Use the "New Routine" option in the menu to start a new routine. If there are unsaved changes, you will be prompted to save them.
- **Quit:** Use the "Quit" option in the menu to exit the application. You will be prompted to save any unsaved changes.

### Task Management

- **Add Task:** Enter the task description and select the time, notification, and repeat options. Click "Add Task" to add it to the list.
- **Delete Task:** Click the delete button next to a task to remove it from the list.
- **Task Order:** Tasks are automatically sorted by notification time.

### Saving and Loading

- **Save Routine:** Save the current list of tasks to a JSON file. You can choose to overwrite an existing file or create a new one.
- **Load Routine:** Load tasks from a previously saved JSON file.

## Contributing

Contributions are welcome! Please follow the steps mentioned in the 'Contributing' section of the README file to contribute to the project.

## License

This project is licensed under the GPL-3.0. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, please open an issue on GitHub.