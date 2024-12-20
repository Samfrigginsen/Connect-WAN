# ConnectWAN - Auto Internet Reconnect Tool

**ConnectWAN** is a Python-based utility that automates reconnecting your internet connection by logging into your TP-LINK Model No. **TL-WR740N** router because it doesn't auto-connect the WAN by itself despite there being settings for it. It monitors internet connectivity and automatically reconnects when disconnected.

---

## Features
- Monitors internet connection in real-time.
- Automatically logs into the router interface and clicks the "Connect" button.
- Displays a message while reconnecting to avoid interference.
- Keeps the browser window on top during the process.
- Runs in the background and can be set to start with Windows.

---

## Requirements
- **Router Model**: TP-LINK TL-WR740N  
  *Note: This tool is specifically designed and tested for this router model.*
- **Operating System**: Windows

---

## How to Use
1. **Run the tool**: Double-click the `.exe` file (or run the Python script).
2. **Start Monitoring**: The program will begin monitoring the internet and reconnect automatically if needed.
3. **Set it to Startup** *(optional)*: Add the program to Windows startup to ensure it runs automatically after boot.

## How to add to Startup

Locate the .exe file inside the dist folder.
Right-click the .exe file and select "Create shortcut".
Copy the shortcut.

Press Win + R to open the Run dialog.
Type shell:startup and press Enter. This opens the Startup folder for the current user.
Paste the shortcut:

Paste the shortcut of your program into the Startup folder.
