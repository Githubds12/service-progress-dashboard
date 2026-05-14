import json
import re

har_path = r"c:\Users\Gorri\Documents\Reports\WebMoneyKeeper\WebMoneyKeeper.har"

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    methods = set()
    for entry in entries:
        url = entry['request']['url']
        if 'api4mini.web.money' in url:
            req_text = entry['request'].get('postData', {}).get('text', '')
            match = re.search(r'<(\w+)\s+xmlns="http://mini\.webmoney\.ru/api">', req_text)
            if match:
                methods.add(match.group(1))
    
    print("Found methods in api4mini.web.money:")
    for m in sorted(methods):
        print(f" - {m}")
except Exception as e:
    print(f"Error: {e}")
