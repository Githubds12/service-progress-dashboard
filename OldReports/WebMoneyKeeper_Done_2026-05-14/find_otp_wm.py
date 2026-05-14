import json

har_path = r"c:\Users\Gorri\Documents\Reports\WebMoneyKeeper\WebMoneyKeeper.har"
otp = "0815"

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    for i, entry in enumerate(entries):
        if otp in json.dumps(entry):
            print(f"--- Entry {i} ---")
            print(f"URL: {entry['request']['url']}")
            print(f"Method: {entry['request']['method']}")
except Exception as e:
    print(f"Error: {e}")
