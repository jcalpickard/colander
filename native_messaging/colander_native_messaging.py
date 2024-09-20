#!/usr/bin/env python3
import sys
import json
import struct
import logging
sys.path.append('./src')
import tabgrab
import tabtally

# Logs messages to a file
# useful for in debugging and understanding the programme's flow
logging.basicConfig(filename='colander_native_messaging.log', level=logging.DEBUG)

logging.debug("Native messaging host started")

# Reads message from standard input
# first reads the length of the message as a 4-byte integer
# then reads the message itself as a UTF-8 encoded string
# finally parses the string as JSON
def get_message():
    raw_length = sys.stdin.buffer.read(4)
    if not raw_length:
        return None
    message_length = struct.unpack('=I', raw_length)[0]
    message = sys.stdin.buffer.read(message_length).decode('utf-8')
    return json.loads(message)

# Sends a message to the host
# first encodes the message as a JSON string
# then encodes the length of the string as a 4-byte integer
# finally writes both to standard output
def send_message(message):
    encoded_message = json.dumps(message).encode('utf-8')
    encoded_length = struct.pack('=I', len(encoded_message))
    sys.stdout.buffer.write(encoded_length)
    sys.stdout.buffer.write(encoded_message)
    sys.stdout.buffer.flush()

def process_tabs(tabs):
    # Here we will implement our tab processing logics
    # for now, we'll count the tabs and return some basic info
    # [!] assumes tabs will always have a domain, which may not be the case
    processed_count = len(tabs)
    unique_domains = len(set(tab.get('url', '').split('/')[2] for tab in tabs if tab.get('url')))
    return {
        "processed_count": processed_count,
        "unique_domains": unique_domains
    }

# Processes message recieved from the host
# checks the action field of the message, performing the corresponding action
# if the action is `get_active_tab`, it calls the function from tabgrab 
# to get the URL and title of the active tab
# if the action is `get_tab_count`, it calls the function from tabtally 
# to get the number of open tabs
# if the action is `process_tabs`, it calls the function 
# to process the tabs in the data field of the message
# if the action is unknown, it returns an error message
def process_message(message):
    try:
        if message['action'] == 'get_active_tab':
            url, title = tabgrab.get_active_tab_info()
            return {'url': url, 'title': title}
        elif message['action'] == 'get_tab_count':
            count = tabtally.get_tab_count()
            return {'tab_count': count}
        elif message['action'] == 'process_tabs':
            return process_tabs(message.get('data', []))
        else:
            return {'error': 'Unknown action'}
    except Exception as e:
        return {'error': str(e)}

# Main loop of the programme
# reads messages from standard input and processes them
# sending results back to the host until there are no more messages
while True:
    try:
        message = get_message()
        if message is None:
            break
        logging.debug(f"Received message: {message}")
        response = process_message(message)
        logging.debug(f"Sending response: {response}")
        send_message(response)
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        break