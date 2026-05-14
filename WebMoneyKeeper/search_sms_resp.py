import json

har_path = r"c:\Users\Gorri\Documents\Reports\WebMoneyKeeper\WebMoneyKeeper.har"

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    for i, entry in enumerate(entries):
        resp_text = entry['response'].get('content', {}).get('text', '')
        if 'sms' in resp_text.lower():
            print(f"--- Entry {i}: {entry['request']['url']} ---")
            print(f"Response (partial): {resp_text[:300]}...")
except Exception as e:
    print(f"Error: {e}")
