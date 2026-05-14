import json
import sys

har_path = 'iHerb/iHerb.har'
with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

for entry in har_data['log']['entries']:
    if 'checkout2.iherb.com' in entry['request']['url']:
        print(f"URL: {entry['request']['url']}")
        for header in entry['request']['headers']:
            print(f"  {header['name']}: {header['value']}")
        print("-" * 50)
        break
