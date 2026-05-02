import json
har_path = r'c:\Users\Gorri\Documents\Reports\Deriv\Deriv.har'
with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for entry in data['log']['entries']:
    url = entry['request']['url']
    method = entry['request']['method']
    if 'registration' in url and method == 'POST':
        print(f"URL: {url}")
        print(f"Body: {entry['request'].get('postData', {}).get('text', 'N/A')}")
        print(f"Response: {entry['response'].get('content', {}).get('text', 'N/A')[:500]}")
        print("-" * 50)
