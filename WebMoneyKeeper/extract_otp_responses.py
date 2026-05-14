import json

har_path = r"c:\Users\Gorri\Documents\Reports\WebMoneyKeeper\WebMoneyKeeper.har"

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    for i, entry in enumerate(entries):
        url = entry['request']['url']
        if 'AccountApi.asmx' in url:
            req_text = entry['request'].get('postData', {}).get('text', '')
            resp_text = entry['response'].get('content', {}).get('text', '')
            if 'SetMobilePhoneNumberEndWithConfirmation' in req_text:
                print(f"--- Entry {i}: {url} ---")
                print(f"Request (code): {req_text[req_text.find('<code>')+6 : req_text.find('</code>')]}")
                print(f"Response: {resp_text}")
                print("-" * 20)
except Exception as e:
    print(f"Error: {e}")
