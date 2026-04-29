import json
import sys

# Set output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

har_path = r'c:\Users\Gorri\Documents\Reports\PaySend\PaySend.har'

with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

entries = har_data['log']['entries']

for entry in entries:
    response = entry['response']
    status = response['status']
    
    if status == 429:
        print(f"Found 429 Rate Limit on: {entry['request']['url']}")
    
    content = response.get('content', {}).get('text', '').lower()
    if 'limit' in content or 'too many' in content or 'cooldown' in content:
        # Check if it's not a false positive (like 'limit_left' or 'no limit')
        if 'rate limit' in content or 'too many requests' in content:
            print(f"Found potential rate limit message in response from: {entry['request']['url']}")
            print(f"Body snippet: {content[:200]}")
