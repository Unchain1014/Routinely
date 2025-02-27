# Routinely  

## Overview  
**Routinely** is a lightweight, open-source daily routine tracker designed for **Linux** and **Windows**. It provides an uncluttered interface while offering essential features such as:  
- Task notifications for reminders  
- Multiple routine tabs for better organization  
- No internet connection or account required  
- Open-source and cross-platform compatibility using PyQt6  

## Features  
- Task management with title, notification time, and repeat options  
- Routine organization with save/load functionality
- Fully local storage with no data sent online  

## Installation  
### Prerequisites  
- Python 3 (Latest version recommended)  
- PyQt6  
- Git (For source installation)  

### Clone and Install  
```bash
git clone git@github.com:Unchain1014/Routinely.git
cd Routinely
pip install -r requirements.txt  # Install dependencies
python src/main.py  # Run the application
```

## File Structure  
```
Routinely/
│── src/
│   ├── main.py               # Main application logic
│   ├── ui/
│   │   ├── design.ui         # Main UI layout
│   │   ├── task_item.ui      # Task item layout
│   │   ├── unsaved_prompt.ui # Unsaved changes prompt
│   │   ├── unsaved_prompt.py # Dialog logic for unsaved changes
│   ├── task_item.py          # Custom task widget
│── .gitignore                # Git ignore file
│── README.md                 # Project documentation
│── requirements.txt          # Python dependencies
```

## Usage  
1. Click "Add Task" and enter task details  
2. Set a notification time if needed  
3. Save, load, and manage routines  
4. Multiple routine tabs (coming soon)  

## Contributing  
Contributions are welcome. To contribute:  
1. Fork the repository  
2. Create a new branch (`git checkout -b feature-name`)  
3. Commit changes (`git commit -m "Added new feature"`)  
4. Push to GitHub (`git push origin feature-name`)  
5. Submit a pull request  

## License  
This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.  

## Contact  
For questions or suggestions, open an **issue** on GitHub.