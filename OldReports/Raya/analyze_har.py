import json
import sys
import io

# Set stdout to use utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

har_path = r'c:\Users\Gorri\Documents\Reports\Raya\Raya.har'

with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for entry in data['log']['entries']:
    request = entry['request']
    url = request['url']
    method = request['method']
    
    # Filter for interesting requests
    if any(k in url.lower() for k in ['raya', 'auth', 'login', 'otp', 'sms', 'verify', 'register', 'send', 'user']):
        print(f"Method: {method}")
        print(f"URL: {url}")
        
        if 'postData' in request:
            print(f"Request Body: {request['postData'].get('text', 'No text content')}")
            
        response = entry['response']
        print(f"Response Status: {response['status']}")
        if 'content' in response:
            print(f"Response Body: {response['content'].get('text', 'No content')}")
        print("-" * 50)
