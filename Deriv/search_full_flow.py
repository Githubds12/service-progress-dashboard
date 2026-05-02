import json
har_path = r'c:\Users\Gorri\Documents\Reports\Deriv\Deriv.har'
with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

keywords = ['registration', 'login', 'settings', 'phone', 'verify', 'otp', 'verification', 'sms', 'code', 'identity']

for i, entry in enumerate(data['log']['entries']):
    url = entry['request']['url']
    method = entry['request']['method']
    
    # Check URL and Body
    body = ""
    if 'postData' in entry['request']:
        body = entry['request']['postData'].get('text', '').lower()
    
    if any(k in url.lower() for k in keywords) or any(k in body for k in keywords):
        # Skip static/noisy files
        if any(url.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.svg', '.woff', '.woff2', '.ttf']):
            continue
        if 'google.com' in url or 'firebase' in url or 'crashlytics' in url or 'appsflyer' in url:
            continue
            
        print(f"Entry {i}: {method} {url}")
        if body:
            print(f"  Body: {body[:1000]}")
        res = entry['response']
        print(f"  Response: {res['status']}")
        if 'content' in res and 'text' in res['content']:
             text = res['content']['text'][:1000].replace('\n', ' ')
             print(f"  Res Body: {text.encode('ascii', 'ignore').decode('ascii')}")
        print("-" * 50)
