import json

har_path = r"c:\Users\Gorri\Documents\Reports\WebMoneyKeeper\WebMoneyKeeper.har"
target_method = "SetMobilePhoneNumberEndWithConfirmation"

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    for i, entry in enumerate(entries):
        req_text = entry['request'].get('postData', {}).get('text', '')
        if target_method in req_text:
            print(f"--- Entry {i}: {entry['request']['url']} ---")
            print(f"Request: {req_text}")
            resp_text = entry['response'].get('content', {}).get('text', 'N/A')
            print(f"Response: {resp_text}")
            print("-" * 20)
except Exception as e:
    print(f"Error: {e}")
