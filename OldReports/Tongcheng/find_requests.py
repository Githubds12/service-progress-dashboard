import json
import sys

# Set output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

har_path = r'c:\Users\Gorri\Documents\Reports\Tongcheng\Tongcheng.har'

with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

entries = har_data['log']['entries']

for i, entry in enumerate(entries):
    request = entry['request']
    url = request['url']
    if 'MemberHandler.ashx' in url:
        print(f"\n--- Index {i}: {request['method']} {url} ---")
        # Print headers
        print("Headers:")
        for header in request.get('headers', []):
            if header['name'].lower() in ['user-dun', 'secsign', 'content-type']:
                print(f"  {header['name']}: {header['value']}")
        
        post_data = request.get('postData', {}).get('text', '')
        if post_data:
            print(f"Request Body: {post_data}")
        
        response = entry['response']
        print(f"Response Status: {response['status']}")
        content = response.get('content', {}).get('text', '')
        if content:
            print(f"Response Body: {content}")
        print("-" * 50)
