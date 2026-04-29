import json

har_path = r'c:\Users\Gorri\Documents\Reports\AMO\AMO.har'

with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

entries = har_data['log']['entries']

for entry in entries:
    request = entry['request']
    if 'api.chatie.love' in request['url']:
        print(f"URL: {request['url']}")
        print(f"Headers: {json.dumps(request['headers'], indent=2)}")
        break
