import json

har_path = r"c:\Users\Gorri\Documents\Reports\Yamaha\Yamaha.har"

with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

for entry in har_data['log']['entries']:
    url = entry['request']['url']
    if "c377768625-eu.com" in url or "yamaha" in url.lower():
        for header in entry['request']['headers']:
            if header['name'].lower() in ['x-requested-with', 'user-agent', 'package']:
                print(f"Header {header['name']}: {header['value']}")
