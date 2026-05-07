import json

har_path = r'c:\Users\Gorri\Documents\Reports\ViyaLite\ViyaLite.har'
with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for entry in data['log']['entries']:
    req = entry['request']
    print(f"{req['method']} {req['url']}")
