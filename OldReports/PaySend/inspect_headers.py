import json

har_path = r'c:\Users\Gorri\Documents\Reports\PaySend\PaySend.har'

with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

entries = har_data['log']['entries']

for entry in entries:
    request = entry['request']
    if 'registration' in request['url']:
        print(f"URL: {request['url']}")
        print(f"Method: {request['method']}")
        print(f"Headers: {json.dumps(request['headers'], indent=2)}")
        print(f"Body: {request.get('postData', {}).get('text', 'N/A')}")
        print("-" * 50)
