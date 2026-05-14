import json

har_path = r"c:\Users\Gorri\Documents\Reports\WebMoneyKeeper\WebMoneyKeeper.har"

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    for i, entry in enumerate(entries):
        url = entry['request']['url']
        if 'SimpleAuthApi.asmx' in url:
            print(f"--- Entry {i}: {url} ---")
            print(f"Request: {entry['request'].get('postData', {}).get('text', 'N/A')}")
            print(f"Response: {entry['response'].get('content', {}).get('text', 'N/A')}")
            print("-" * 20)
except Exception as e:
    print(f"Error: {e}")
