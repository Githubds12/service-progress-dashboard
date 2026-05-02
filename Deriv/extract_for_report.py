import json
har_path = r'c:\Users\Gorri\Documents\Reports\Deriv\Deriv.har'
with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for i, entry in enumerate(data['log']['entries']):
    url = entry['request']['url']
    method = entry['request']['method']
    body = entry['request'].get('postData', {}).get('text', '')
    
    if ('registration' in url and method == 'POST') or \
       ('login' in url and method == 'POST' and 'verify_phone' in body) or \
       ('settings' in url and method == 'POST'):
        
        print(f"### Entry {i}")
        print(f"**URL**: `{url}`")
        print(f"**Method**: `{method}`")
        print("**Request Headers**:")
        print("```")
        for h in entry['request']['headers']:
            print(f"{h['name']}: {h['value']}")
        print("```")
        print("**Request Body**:")
        print("```json")
        print(body)
        print("```")
        
        res = entry['response']
        print(f"**Response Status**: `{res['status']}`")
        print("**Response Body**:")
        print("```json")
        print(res.get('content', {}).get('text', 'N/A'))
        print("```")
        print("-" * 100)
