import json

har_path = r"c:\Users\Gorri\Documents\Reports\WebMoneyKeeper\WebMoneyKeeper.har"
targets = ['SimpleAuthApi.asmx', 'SmsApi.asmx', 'AppActivationApi.asmx']

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    for i, entry in enumerate(entries):
        url = entry['request']['url']
        if any(t in url for t in targets):
            print(f"--- Entry {i}: {url} ---")
            post_data = entry['request'].get('postData', {}).get('text', 'N/A')
            print(f"Request Body: {post_data[:500]}...")
            resp_text = entry['response'].get('content', {}).get('text', 'N/A')
            print(f"Response Body: {resp_text[:500]}...")
            print("-" * 20)
except Exception as e:
    print(f"Error: {e}")
