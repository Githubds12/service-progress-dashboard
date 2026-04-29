import json
import sys

# Set output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

har_path = r'c:\Users\Gorri\Documents\Reports\Tongcheng\Tongcheng.har'

with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

entries = har_data['log']['entries']

for i, entry in enumerate(entries):
    request = entry['request']
    if 'MemberHandler.ashx' in request['url']:
        print(f"Index {i}: {request['url']}")
