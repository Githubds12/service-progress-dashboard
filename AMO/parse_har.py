import json
import sys

# Set output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

har_path = r'c:\Users\Gorri\Documents\Reports\AMO\AMO.har'

with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

entries = har_data['log']['entries']

print(f"Total entries: {len(entries)}")

# 1. Look for App Details in headers
app_details = set()
for entry in entries:
    request = entry['request']
    for header in request.get('headers', []):
        if 'package' in header['name'].lower() or 'user-agent' in header['name'].lower():
            if 'amo' in header['value'].lower():
                app_details.add(f"{header['name']}: {header['value']}")

print("\nPotential App Details:")
for detail in app_details:
    print(detail)

# 2. Search for Registration/Auth flow
print("\n--- Registration/Auth Flow Search ---")
keywords = ['register', 'auth', 'otp', 'phone', 'sms', 'login', 'verify']
for entry in entries:
    request = entry['request']
    url = request['url']
    method = request['method']
    post_data = request.get('postData', {}).get('text', '')
    
    if any(kw in url.lower() for kw in keywords) or any(kw in post_data.lower() for kw in keywords):
        print(f"\n[{method}] {url}")
        if post_data:
            print(f"Request Body: {post_data[:500]}...")
        
        response = entry['response']
        print(f"Response Status: {response['status']}")
        content = response.get('content', {})
        if 'text' in content:
            print(f"Response Body: {content['text'][:500]}...")
        print("-" * 50)
