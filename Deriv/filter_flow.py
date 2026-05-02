import json
har_path = r'c:\Users\Gorri\Documents\Reports\Deriv\Deriv.har'
with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
for i, entry in enumerate(data['log']['entries']):
    url = entry['request']['url']
    if 'self-service' in url or 'oryapis.com' in url or 'deriv' in url:
        req = entry['request']
        # Filter out static assets
        if any(url.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.svg']):
             continue
        print(f"Entry {i}: {req['method']} {url}")
        if 'postData' in req:
            print(f"  Body: {req['postData'].get('text', 'N/A')[:1000]}")
        res = entry['response']
        print(f"  Response: {res['status']}")
        if 'content' in res and 'text' in res['content']:
             text = res['content']['text'][:1000].replace('\n', ' ')
             print(f"  Res Body: {text.encode('ascii', 'ignore').decode('ascii')}")
        print("-" * 50)
