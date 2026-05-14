import json
import base64

har_path = r'c:\Users\Gorri\Documents\Reports\Yaahlan\yaahlan.har'

with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data['log']['entries']

print(f"Total entries: {len(entries)}")

for i, entry in enumerate(entries):
    request = entry['request']
    response = entry['response']
    url = request['url']
    
    # Common keywords for OTP flows
    if any(k in url.lower() for k in ['login', 'otp', 'send', 'verify', 'auth', 'sms', 'mobile', 'phone']):
        print(f"\n[{i}] {request['method']} {url}")
        print(f"Status: {response['status']}")
        
        # Request body
        if 'postData' in request:
            print(f"Request body: {request['postData'].get('text', 'N/A')}")
            
        # Response body
        if 'content' in response and 'text' in response['content']:
            text = response['content']['text']
            if response['content'].get('encoding') == 'base64':
                try:
                    text = base64.b64decode(text).decode('utf-8', errors='replace')
                except:
                    text = "[Binary/Base64]"
            print(f"Response body: {text[:500]}...")
