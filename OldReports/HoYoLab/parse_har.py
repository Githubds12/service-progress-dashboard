import json

har_path = r'c:\Users\Gorri\Documents\Reports\HoYoLab\HoYoLab.har'

with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data['log']['entries']
relevant_entries = []

keywords = ['hoyoverse.com', 'mihoyo.com', 'account', 'passport', 'login', 'otp', 'verify']

for entry in entries:
    url = entry['request']['url']
    if any(kw in url.lower() for kw in keywords):
        relevant_entries.append(entry)

print(f"Found {len(relevant_entries)} relevant entries.")

for entry in relevant_entries:
    req = entry['request']
    res = entry['response']
    url = req['url']
    method = req['method']
    
    if method == 'POST':
        print(f"Method: {method}, URL: {url}")
        print(f"Post Data: {req.get('postData', {}).get('text', 'N/A')[:500]}")
        print(f"Response Status: {res['status']}")
        print(f"Response Body: {res.get('content', {}).get('text', 'N/A')[:200]}")
        print("-" * 50)
