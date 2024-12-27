# Windev Discord Presence

![Windev Discord Presence](https://windev.com/img/2025/develop-10-times-faster.webp)

This project integrates **WinDev** with **Discord Rich Presence**, allowing you to display real-time information about the project and file you are working on in WinDev directly on your Discord profile.

With this tool, you can elegantly and dynamically share your development activities and productivity with friends and colleagues.

---

## Features

- Displays the **project/workspace** currently open in WinDev.
- Shows the **name of the file** being edited.
- Dynamically updates the Discord status while you edit files in WinDev.

---

## How to Set Up and Use

### 1. **Prerequisites**

Make sure you have Python installed (recommended version: Python 3.10 or higher).

Before running the application, install the project dependencies using the `requirements.txt` file. Run the following command in your terminal:

```pip install -r requirements.txt```



### 2. **Create a Client ID on Discord**

To use Discord Rich Presence, you need a **Client ID**. Follow these steps:

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Log in with your Discord account.
3. Click on **New Application**.
4. Give your application a name (e.g., "WinDev Presence").
5. Copy the **Client ID** displayed on the application's main page.

---

## 3. **Replace the Client ID in the Code**

After obtaining your **Client ID**, open the `WindevDiscordPresence.py` file in your preferred text editor and locate the following line:


```CLIENT_ID = "YOUR_CLIENT_ID_HERE"```

### 4. **Compile the Script into an Executable**

To create a standalone executable, follow these steps:

Make sure you have `pyinstaller` installed. If not, install it using the command:

`pip install pyinstaller`

Compile the script into a single executable file with the following command:

`pyinstaller --onefile --windowed --icon=icon.ico WindevDiscordPresence.py`

### 5. **Run the Application**

1. Double-click the generated executable file (`WindevDiscordPresence.exe`) located in the `dist` folder.
2. The application will start running in the background.
3. You can access it via the system tray icon. Right-click the icon to open the menu or exit the application.
4. While editing in WinDev, your Discord Rich Presence will automatically update with the project and file information.

---

### Optional: **Download the Executable**

If you prefer not to compile the script yourself, you can download the precompiled executable from the link below:

[Download Executable](https://github.com/fmartns/WindevDiscordPresence/releases/download/Alpha/WindevDiscordPresence.exe)

This will allow you to skip the compilation steps and immediately start using the tool.

---
