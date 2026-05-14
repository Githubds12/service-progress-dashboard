import json

har_path = r'c:\Users\Gorri\Documents\Reports\nextBike\nextBike.har'

with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data['log']['entries']

for entry in entries:
    req = entry['request']
    url = req['url']
    if 'GbHsVs75zIp' in url or 'GbHsVs75zIp' in str(req):
        print(f"Found app_hash in request: {url}")
        print(f"Method: {req['method']}")
        print(f"Status: {entry['response']['status']}")
        print("-" * 50)
