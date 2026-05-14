import json

har_path = r"c:\Users\Gorri\Documents\Reports\WebMoneyKeeper\WebMoneyKeeper.har"
otp = "0815"

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    for i, entry in enumerate(entries):
        entry_json = json.dumps(entry)
        if otp in entry_json:
            print(f"--- Entry {i}: {entry['request']['url']} ---")
            print(f"Method: {entry['request']['method']}")
            # Check if it's in request or response
            if otp in json.dumps(entry['request']):
                print("Found in Request")
            if otp in json.dumps(entry['response']):
                print("Found in Response")
except Exception as e:
    print(f"Error: {e}")
