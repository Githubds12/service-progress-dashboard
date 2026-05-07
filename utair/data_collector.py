import json
import base64
import os

# This script will be executed by the model after it fetches all necessary data.
# However, I can't easily fetch data in a loop inside a tool call.
# I'll have to do it in batches using the available tools.

# I'll create a list of all IDs and then use a series of tool calls to get the data.
event_ids = [f"287967-{i}" for i in range(34)]

# I'll store the collected data in a temporary JSON file.
temp_data_file = "temp_collected_data.json"

def save_event_data(event_id, outline, req_body, resp_body):
    if os.path.exists(temp_data_file):
        with open(temp_data_file, 'r') as f:
            data = json.load(f)
    else:
        data = {}
    
    data[event_id] = {
        "outline": outline,
        "request_body": req_body,
        "response_body": resp_body
    }
    
    with open(temp_data_file, 'w') as f:
        json.dump(data, f)

# I will provide this script for the model to use as a helper if needed, 
# but I'll mostly rely on tool calls for data retrieval.
