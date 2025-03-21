# Routinely  

## Overview  
**Routinely** is a lightweight, open-source daily routine tracker designed for **Linux** and **Windows**. It provides an uncluttered interface while offering essential features such as:  
- Task management with title, notification time, and repeat options  
- Multiple routine tabs for better organization (future goal)  
- No internet connection or account required  
- Routines stored in human-readable JSON files  
- Open-source and cross-platform compatibility using PyQt6  
- System tray implementation so you never miss a notification  
- User interface theme follows OS light/dark preference and theme colors  

It is designed to look and feel like a workplace daily scheduler and can be used for this purpose. When it is time to notify about a task, a dialog window will pop up and steal focus until user confirmation. A custom sound will play on loop until the notification dialog window is acknowledged (replace "/sounds/notification.wav" to change this sound).

![screenshot.png](/images/screenshot.png)

![screenshot2.png](/images/screenshot2.png)

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

## Contributing  
Contributions are welcome. To contribute:  
1. Fork the repository  
2. Create a new branch (`git checkout -b feature-name`)  
3. Commit changes (`git commit -m "Added new feature"`)  
4. Push to GitHub (`git push origin feature-name`)  
5. Submit a pull request  

## License  
This project is licensed under the **GPL-3.0**. See [LICENSE](LICENSE) for details.  

## Contact  
For questions or suggestions, open an **issue** on GitHub.
