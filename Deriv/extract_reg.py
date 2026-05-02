import json
har_path = r'c:\Users\Gorri\Documents\Reports\Deriv\Deriv.har'
with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for i, entry in enumerate(data['log']['entries']):
    url = entry['request']['url']
    method = entry['request']['method']
    if 'registration' in url and method == 'POST':
        print(f"### Entry {i}")
        print(f"**URL**: `{url}`")
        print(f"**Method**: `{method}`")
        print("**Request Body**:")
        print(entry['request'].get('postData', {}).get('text', ''))
        print("**Response Body**:")
        print(entry['response'].get('content', {}).get('text', ''))
        print("-" * 100)
