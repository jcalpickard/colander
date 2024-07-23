# TABGRAB.PY
# retrieves the active tab's URL and title
# and appends this information to a text file with a timestamp

# Using Firefox's recovery.jsonlz4 file to extract the active tab's information
# is a creative and effective solution

# However, the script's ability to extract and manipulate data about web browsing 
# can be seen as a form of surveillance
# with implications for privacy, power, and control

import lz4.block
import json
import os
import datetime

# Opens the sessionstore.jsonlz4 file
# decompresses it using the lz4 library, and then loads the JSON data
# iterates over the windows and tabs in the JSON data to find the active tab 
# then returns its URL and title
def get_active_tab_info():
    # Replace with your Firefox profile path
    profile_path = r"C:\Users\Cal\AppData\Roaming\Mozilla\Firefox\Profiles\m76qq8d6.default-release"
    session_file = os.path.join(profile_path, r"sessionstore-backups\previous.jsonlz4")

    if not os.path.exists(session_file):
        print(f"File not found: {session_file}")
        return None, None

    with open(session_file, "rb") as f:
        data = f.read()
        decompressed = lz4.block.decompress(data[8:])
        json_data = json.loads(decompressed)

    for window in json_data.get("windows", []):
        for tab in window.get("tabs", []):
            if tab.get("index") == window.get("selected"):
                entry = tab["entries"][-1]
                return entry.get("url"), entry.get("title")

    return None, None
    pass # This is currently stopping it being appended to the text file?

# Takes the URL and title of the active tab as arguments
# generates a timestamp
# then appends this information to a text file
def save_tab_info(url, title):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("tab_capture.txt", "a") as f:
        f.write(f"{timestamp} - {title}: {url}\n")

if __name__ == "__main__":
    url, title = get_active_tab_info()
    if url and title:
        save_tab_info(url, title)
        print(f"Captured: {title}")
    else:
        print("Failed to capture tab info")