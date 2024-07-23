# TABGRAB2.PY
# another approach to retrieving the active tab's URL and title
# because my first prototypes didn't have access to real-time information

# Trying pyautogui, as a way to roll up an ersatz browser user

import pyautogui
import time
from datetime import datetime

def capture_current_tab():
    # Activate the address bar
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.1)
    
    # Copy the URL
    pyautogui.hotkey('ctrl', 'c')
    url = pyautogui.paste()
    
    # Get the window title (assumes it's the tab title)
    title = pyautogui.getActiveWindowTitle()
    
    # Save to file
    with open("captured_tabs.txt", "a") as f:
        f.write(f"{datetime.now()} - {title}: {url}\n")

if __name__ == "__main__":
    capture_current_tab()