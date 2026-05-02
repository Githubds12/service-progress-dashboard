import json
har_path = r'c:\Users\Gorri\Documents\Reports\Deriv\Deriv.har'
with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
for i, entry in enumerate(data['log']['entries']):
    url = entry['request']['url']
    if 'oryapis.com' in url:
        req = entry['request']
        print(f"Entry {i}: {req['method']} {url}")
        if 'postData' in req:
            print(f"  Body: {req['postData'].get('text', 'N/A')}")
        res = entry['response']
        print(f"  Response: {res['status']}")
        if 'content' in res and 'text' in res['content']:
             print(f"  Res Body: {res['content']['text'][:500]}")
        print("-" * 50)
