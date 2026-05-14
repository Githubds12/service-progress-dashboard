import json
import os

har_path = r'c:\Users\Gorri\Documents\Reports\Medal\Medal.har'

with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data['log']['entries']
for i, entry in enumerate(entries):
    request = entry['request']
    url = request['url']
    method = request['method']
    
    if any(k in url.lower() for k in ['/sms', '/settings', '/auth']):
        print(f"Index: {i}")
        print(f"Method: {method}")
        print(f"URL: {url}")
        
        if 'postData' in request:
            print(f"Request Body: {request['postData'].get('text', 'No text content')}")
            
        response = entry['response']
        print(f"Response Status: {response['status']}")
        if 'content' in response:
            text = response['content'].get('text', '')
            if len(text) > 300:
                text = text[:300] + "... [Truncated]"
            print(f"Response Body: {text}")
        print("-" * 50)
