import json
import re

har_path = r"c:\Users\Gorri\Documents\Reports\Yamaha\Yamaha.har"

with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

version_pattern = re.compile(r'\d+\.\d+\.\d+')

for entry in har_data['log']['entries']:
    # Check headers
    for header in entry['request']['headers']:
        if version_pattern.search(header['value']):
            print(f"Header {header['name']}: {header['value']}")
            
    # Check post data
    if 'postData' in entry['request'] and 'text' in entry['request']['postData']:
        text = entry['request']['postData']['text']
        match = version_pattern.search(text)
        if match:
            print(f"Post Data: {text[:200]}")
