import json
import os

har_path = r'c:\Users\Gorri\Documents\Reports\Deriv\Deriv.har'
with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data['log']['entries']
for i, entry in enumerate(entries):
    req = entry['request']
    url = req['url']
    method = req['method']
    
    # Filter for interesting keywords
    interesting = ['verify', 'otp', 'login', 'signup', 'auth', 'phone', 'email', 'mobile', 'sms', 'deriv']
    if any(k in url.lower() for k in interesting) or method == 'POST':
        try:
            print(f"Entry {i}: {method} {url}")
            if 'postData' in req:
                print(f"  Body: {req['postData'].get('text', 'N/A')[:500]}")
            res = entry['response']
            print(f"  Response: {res['status']} {res['statusText']}")
            if 'content' in res and 'text' in res['content']:
                text = res['content']['text'][:1000].replace('\n', ' ')
                print(f"  Res Body: {text.encode('ascii', 'ignore').decode('ascii')}")
            print("-" * 50)
        except Exception as e:
            print(f"Error printing entry {i}: {e}")
