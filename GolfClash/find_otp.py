import json

har_path = r"c:\Users\Gorri\Documents\Reports\GolfClash\GolfClash.har"
otp = "6197"

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    for i, entry in enumerate(entries):
        entry_str = json.dumps(entry)
        if otp in entry_str:
            print(f"--- Entry {i} ---")
            print(f"URL: {entry['request']['url']}")
            print(f"Method: {entry['request']['method']}")
            # Find which part contains the OTP
            if otp in json.dumps(entry['request']):
                print("Found in Request")
            if otp in json.dumps(entry['response']):
                print("Found in Response")
except Exception as e:
    print(f"Error: {e}")
