import json
import sys

# Set output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

har_path = r'c:\Users\Gorri\Documents\Reports\Tongcheng\Tongcheng.har'

with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

entries = har_data['log']['entries']
target = "6b4ff8ae36a68ee1fc7fab3a57f98e26"

for i, entry in enumerate(entries):
    request = entry['request']
    for header in request.get('headers', []):
        if target in header['value']:
            print(f"Index {i} Header: {header['name']}")
    for cookie in request.get('cookies', []):
        if target in cookie['value']:
            print(f"Index {i} Cookie: {cookie['name']}")
