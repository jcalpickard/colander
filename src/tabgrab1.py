# TABGRAB1.PY
# retrieves the active tab's URL and title
# and appends this information to a text file with a timestamp

import lz4.block
import json
import os
import datetime

def get_firefox_profile_path():
    # This path might need to be adjusted for your system
    return os.path.expanduser('~/AppData/Roaming/mozilla/firefox')

def find_default_profile(profile_path):
    with open(os.path.join(profile_path, 'profiles.ini'), 'r') as f:
        for line in f:
            if line.startswith('Path=') and 'default' in line:
                return line.split('=')[1].strip()
    return None

def get_tab_info():
    profile_path = get_firefox_profile_path()
    default_profile = find_default_profile(profile_path)
    if not default_profile:
        print("Default profile not found.")
        return

    session_file = os.path.join(profile_path, default_profile, 'sessionstore-backups', 'previous.jsonlz4')
    
    if not os.path.exists(session_file):
        print(f"Session file not found: {session_file}")
        return

    with open(session_file, "rb") as f:
        data = f.read()
        decompressed = lz4.block.decompress(data[8:])
        json_data = json.loads(decompressed)

    tabs = []
    for window in json_data.get("windows", []):
        for tab in window.get("tabs", []):
            entry = tab["entries"][-1]
            tabs.append((entry.get("url"), entry.get("title")))

    return tabs

def save_tab_info(tabs):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("tab_capture.txt", "a") as f:
        f.write(f"\n--- Capture at {timestamp} ---\n")
        for url, title in tabs:
            f.write(f"{title}: {url}\n")

if __name__ == "__main__":
    tabs = get_tab_info()
    if tabs:
        save_tab_info(tabs)
        print(f"Captured {len(tabs)} tabs")
    else:
        print("Failed to capture tab info")