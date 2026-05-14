import json
import sys

# Set output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

har_path = r'c:\Users\Gorri\Documents\Reports\Tongcheng\Tongcheng.har'

with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

entries = har_data['log']['entries']

for i in [951, 987, 993, 994, 995]:
    request = entries[i]['request']
    print(f"\n--- Index {i}: {request['method']} {request['url']} ---")
    post_data = request.get('postData', {}).get('text', '')
    print(f"Request Body: {post_data}")
    
    response = entries[i]['response']
    print(f"Response Status: {response['status']}")
    content = response.get('content', {}).get('text', '')
    print(f"Response Body: {content}")
    print("-" * 50)
