import json

har_path = r"c:\Users\Gorri\Documents\Reports\WebMoneyKeeper\WebMoneyKeeper.har"

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    for i, entry in enumerate(entries):
        req_text = entry['request'].get('postData', {}).get('text', '')
        if 'SetMobilePhoneNumber' in req_text:
            print(f"--- Entry {i}: {entry['request']['url']} ---")
            # Extract the method name
            import re
            method = re.search(r'<(\w+)\s', req_text)
            print(f"Method: {method.group(1) if method else 'Unknown'}")
            print(f"Request: {req_text[:500]}...")
except Exception as e:
    print(f"Error: {e}")
