# TABTALLY.PY

import lz4.block
import json
import os

def get_tab_count():
    profile_path = r"C:\Users\Cal\AppData\Roaming\Mozilla\Firefox\Profiles\e46pq4hi.default"
    session_file = os.path.join(profile_path, "sessionstore.jsonlz4")

    if not os.path.exists(session_file):
        print(f"File not found: {session_file}")
        return 0

    with open(session_file, "rb") as f:
        data = f.read()
        decompressed = lz4.block.decompress(data[8:])
        json_data = json.loads(decompressed)

    tab_count = sum(len(window.get("tabs", [])) for window in json_data.get("windows", []))
    return tab_count

if __name__ == "__main__":
    count = get_tab_count()
    print(f"Total open tabs: {count}")