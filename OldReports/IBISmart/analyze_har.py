import json
import sys
import io

# Set stdout to use utf-8 to avoid UnicodeEncodeError
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

har_path = r'c:\Users\Gorri\Documents\Reports\IBISmart\IBISmart.har'

with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for entry in data['log']['entries']:
    request = entry['request']
    url = request['url']
    method = request['method']
    
    if '/api/onboarding/otp/' in url:
        print(f"Method: {method}")
        print(f"URL: {url}")
        print("Request Headers:")
        for h in request['headers']:
            print(f"  {h['name']}: {h['value']}")
        
        if 'postData' in request:
            print(f"Request Body: {request['postData'].get('text', 'No text content')}")
            
        response = entry['response']
        print(f"Response Status: {response['status']}")
        print("Response Headers:")
        for h in response['headers']:
            print(f"  {h['name']}: {h['value']}")
        if 'content' in response:
            print(f"Response Body: {response['content'].get('text', 'No content')}")
        print("-" * 50)
