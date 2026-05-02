import json

har_file = r'c:\Users\Gorri\Documents\Reports\Flowwow\Flowwow.har'

with open(har_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data['log']['entries']

print(f"Total entries: {len(entries)}")

for i, entry in enumerate(entries):
    request = entry['request']
    url = request['url']
    method = request['method']
    
    # Filter for relevant keywords
    keywords = ['sms', 'auth', 'otp', 'send', 'login', 'register', 'verify', 'phone']
    if any(keyword in url.lower() for keyword in keywords):
        print(f"[{i}] {method} {url}")
        
        # Print request body if exists
        if 'postData' in request and 'text' in request['postData']:
            print(f"  Request body: {request['postData']['text']}")
        
        # Print response if exists
        response = entry['response']
        print(f"  Response status: {response['status']}")
        if 'content' in response and 'text' in response['content']:
            text = response['content']['text']
            if len(text) > 200:
                text = text[:200] + "..."
            print(f"  Response body: {text}")
        print("-" * 20)
