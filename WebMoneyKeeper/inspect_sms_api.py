import json

har_path = r"c:\Users\Gorri\Documents\Reports\WebMoneyKeeper\WebMoneyKeeper.har"

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    for i, entry in enumerate(entries):
        url = entry['request']['url']
        if 'SmsApi.asmx' in url:
            req_text = entry['request'].get('postData', {}).get('text', '')
            # Look for common auth keywords in XML
            if any(k in req_text.lower() for k in ['verify', 'check', 'auth', 'confirm', 'login']):
                print(f"--- Entry {i}: {url} ---")
                print(f"Request: {req_text[:300]}...")
except Exception as e:
    print(f"Error: {e}")
