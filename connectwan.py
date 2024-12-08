# Section 1: Import Libraries
import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pywinauto import Desktop
import pygetwindow as gw
import pyautogui  # Add PyAutoGUI import
import time
import pystray
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import tkinter as tk


# Function to minimize to tray
def send_to_tray():
    # Create an icon for the system tray
    def create_image():
        # Create a blank image with a circle (as a placeholder icon)
        image = Image.new("RGB", (64, 64), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.ellipse((16, 16, 48, 48), fill=(0, 128, 255))
        return image

    def on_exit(icon, item):
        icon.stop()
        root.destroy()

    def on_show(icon, item):
        root.deiconify()  # Show the window again
        icon.stop()

    # Create the tray menu
    menu = Menu(MenuItem("Show", on_show), MenuItem("Exit", on_exit))

    # Create and start the tray icon
    tray_icon = Icon("ConnectWAN", create_image(), "ConnectWAN", menu)
    tray_icon.run_detached()
    root.withdraw()  # Hide the main window


# Section 2: Paths to Brave Browser and ChromeDriver
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
driver_path = r"F:\Programming\chromedriver-win64\chromedriver.exe"


# Section: Bring Browser to Top and Keep it Focused
def bring_browser_to_top():
    try:
        # Get the browser window title
        windows = gw.getAllTitles()
        browser_window = next(
            (w for w in windows if "Brave" in w or "Chrome" in w), None
        )

        if browser_window:
            # Use pywinauto to set the window to stay on top
            app = Desktop(backend="uia").window(title=browser_window)
            app.set_focus()
            app.topmost = True  # Ensure it's always on top
            print(f"Browser window '{browser_window}' is now on top.")
        else:
            print("Browser window not found.")
    except Exception as e:
        print(f"Error setting browser to top: {e}")


# Section 3: Check internet connectivity
def check_internet(url="http://www.google.com", timeout=5):
    try:
        requests.get(url, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False


# Section 4: Find and Click the Connect Button using PyAutoGUI
def find_and_click_connect_button(driver):
    try:
        # Wait for the page to load
        time.sleep(3)

        # Now press the Tab key 20 times
        for _ in range(20):
            pyautogui.press("tab")
            time.sleep(0.1)  # Short delay to simulate pressing tab

        # Step 5: Press Enter after Tabbing
        pyautogui.press("enter")
        time.sleep(1)  # Wait for the action to complete

        print("Pressed Tab 20 times and then Enter.")

        print("Reconnected to WAN successfully!")

    except Exception as e:
        print(f"Error: {e}")


# Section 5: Reconnect to the router
def connect_to_router():
    try:

        # Set up Selenium for Brave
        options = webdriver.ChromeOptions()
        options.binary_location = brave_path
        driver = webdriver.Chrome(service=Service(driver_path), options=options)

        # Access the router settings page
        driver.get("http://192.168.0.1")
        time.sleep(3)

        # Step 1: Locate the username field and enter the username
        username_field = driver.find_element(By.ID, "userName")
        username_field.send_keys("admin")

        # Step 2: Locate the password field and enter the password
        password_field = driver.find_element(By.ID, "pcPassword")
        password_field.send_keys("admin")

        # Step 3: Locate and click the login button
        login_button = driver.find_element(By.ID, "loginBtn")
        login_button.click()
        time.sleep(2)  # Wait for the next page to load

        # Step 4: Call the function to find and click the "Connect" button
        find_and_click_connect_button(driver)

        # Wait for 5 seconds before closing the browser
        time.sleep(10)

    except Exception as e:
        log_message(f"Error: {e}")
    finally:
        driver.quit()


# Section 6: Start monitoring for internet connectivity
def start_monitoring():
    global monitoring
    monitoring = True
    log_message("Started monitoring for internet connection.")
    thread = threading.Thread(target=monitor_connection, daemon=True)
    thread.start()


# Section 7: Stop monitoring
def stop_monitoring():
    global monitoring
    monitoring = False
    log_message("Stopped monitoring for internet connection.")


# Section 8: Monitor connection and attempt reconnection if needed
def monitor_connection():
    while monitoring:
        if check_internet():
            update_status("Connected", "green")
        else:
            update_status("Disconnected", "red")
            log_message("Internet disconnected. Attempting to reconnect...")
            connect_to_router()
        time.sleep(10)  # Check every 10 seconds


# Section 9: Log messages to the GUI
def log_message(message):
    log_box.config(state=tk.NORMAL)
    log_box.insert(tk.END, f"{message}\n")
    log_box.see(tk.END)
    log_box.config(state=tk.DISABLED)


# Section 10: Update the internet status label
def update_status(status, color):
    status_label.config(text=f"Internet Status: {status}", fg=color)


# Section 11: GUI setup
root = tk.Tk()
root.title("Internet Reconnection Monitor")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

# Internet status label
status_label = tk.Label(frame, text="Internet Status: Unknown", font=("Arial", 14))
status_label.pack(pady=10)

# Start/Stop buttons
start_button = tk.Button(
    frame,
    text="Start Monitoring",
    command=start_monitoring,
    font=("Arial", 12),
    bg="green",
    fg="white",
)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = tk.Button(
    frame,
    text="Stop Monitoring",
    command=stop_monitoring,
    font=("Arial", 12),
    bg="red",
    fg="white",
)
stop_button.pack(side=tk.RIGHT, padx=10)

# Log box for displaying logs
log_box = scrolledtext.ScrolledText(
    frame, width=50, height=15, state=tk.DISABLED, font=("Courier", 10)
)
log_box.pack(pady=10)

send_to_tray_button = tk.Button(
    frame,
    text="Send to Tray",
    command=send_to_tray,
    font=("Arial", 12),
    bg="blue",
    fg="white",
)
send_to_tray_button.pack(pady=10)

# Initialize monitoring state
monitoring = False

# Start monitoring immediately when the script is executed (outside of the GUI)
start_monitoring()  # This will automatically start monitoring

# Section 12: Start the GUI event loop
root.mainloop()
