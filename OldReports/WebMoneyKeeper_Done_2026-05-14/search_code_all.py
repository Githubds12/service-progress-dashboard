import json

har_path = r"c:\Users\Gorri\Documents\Reports\WebMoneyKeeper\WebMoneyKeeper.har"

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    for i, entry in enumerate(entries):
        req_text = entry['request'].get('postData', {}).get('text', '').lower()
        if 'code' in req_text and 'api' in entry['request']['url']:
            print(f"--- Entry {i}: {entry['request']['url']} ---")
            print(f"Request: {entry['request'].get('postData', {}).get('text', '')[:500]}...")
            print(f"Response: {entry['response'].get('content', {}).get('text', '')[:500]}...")
            print("-" * 20)
except Exception as e:
    print(f"Error: {e}")
