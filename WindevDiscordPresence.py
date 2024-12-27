import psutil
import time
from pypresence import Presence
import pygetwindow as gw
import pyautogui
import win32gui
import re
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import threading

project_name = None
current_window_name = None
last_window_name = None

CLIENT_ID = "1318565869798031370"  # Discord Application Client ID
APPLICATION_NAME = "W"  # The name of the application (WinDev)

# Function to create the system tray icon image
def create_image():
    image = Image.new('RGB', (64, 64), color=(255, 255, 255))  # White background
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 64, 64), fill="blue")  # Blue rectangle as an example
    return image

# Function to quit the tray icon when the user clicks "Exit"
def on_quit(icon, item):
    icon.stop()  # Stops the icon when the user clicks "Exit"

# Function to enumerate through open windows and find the relevant WinDev project name and window title
def winEnumHandler(hwnd, ctx):
    global project_name, current_window_name
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if "WINDEV" in title.upper():
            parts = title.split(" - ")
            if len(parts) >= 2:
                project_name = parts[0].strip()  # Extract project name
                matches = re.findall(r'\[([^\]]+)\]', title)  # Extract window name within brackets
                if len(matches) >= 1:
                    window_text = matches[0]
                    window_text_cleaned = re.sub(r'\(.*?\)', '', window_text).strip()  # Clean window title text
                    current_window_name = window_text_cleaned

# Function to get the current active window name
def get_current_window_name():
    win32gui.EnumWindows(winEnumHandler, None)
    return current_window_name

# Function to get the current active WinDev project name
def get_windev_project_name():
    win32gui.EnumWindows(winEnumHandler, None)
    return project_name

# Function to get the start time of the WinDev application process
def get_windev_start_time():
    for proc in psutil.process_iter(attrs=['pid', 'name', 'create_time']):
        try:
            if APPLICATION_NAME.lower() in proc.info['name'].lower():  # Match process name
                return proc.info['create_time']  # Return process start time
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return None

# Function to get the uptime (time since the WinDev application started)
def get_windev_uptime():
    for proc in psutil.process_iter(attrs=['pid', 'name', 'create_time']):
        try:
            if APPLICATION_NAME.lower() in proc.info['name'].lower():  # Match process name
                return time.time() - proc.info['create_time']  # Calculate uptime
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return None

# Function to update the Discord presence with project and window information
def update_discord_presence():
    global last_window_name
    try:
        RPC = Presence(CLIENT_ID)  # Create Discord Presence object
        RPC.connect()  # Connect to Discord
        print("Connected to Discord Rich Presence.")
        start_time = get_windev_start_time()  # Get the application start time

        while True:
            uptime = get_windev_uptime()  # Get the uptime of WinDev application
            current_window_name = get_current_window_name()  # Get the current active window name
            project_name = get_windev_project_name()  # Get the current WinDev project name

            if current_window_name != last_window_name:  # Check if window name changed
                last_window_name = current_window_name  # Update the last window name
                start_time = time.time()  # Reset the start time

            if uptime and current_window_name and project_name:
                uptime_formatted = time.strftime("%H:%M:%S", time.gmtime(uptime))  # Format uptime
                RPC.update(  # Update Discord Rich Presence
                    state=f"Editing {current_window_name}",
                    details=f"Workspace {project_name}",
                    large_image="windev_logo",
                    large_text="WinDev IDE",
                    start=start_time
                )
            else:
                print("WinDev is not open or an active display was not found.")
                RPC.clear()  # Clear presence if WinDev is not active

            time.sleep(1)  # Wait for 1 second before updating again
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)  # Wait for 5 seconds before retrying

# Function to start the system tray icon in a separate thread
def start_tray_icon():
    icon = Icon("DiscordPresence", create_image(), menu=Menu(MenuItem('Exit', on_quit)))  # Create tray icon with menu
    icon.run()  # Run the tray icon

# Main function to launch the Discord presence and tray icon
if __name__ == "__main__":
    # Start the tray icon in a separate thread
    tray_thread = threading.Thread(target=start_tray_icon, daemon=True)
    tray_thread.start()

    # Start updating the Discord presence
    print("Launching the Discord Presence application for WinDev...")
    update_discord_presence()  # Start updating Discord presence
