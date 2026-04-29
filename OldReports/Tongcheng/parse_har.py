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
    if request['method'] == 'POST' and ('17u.cn' in request['url'] or 'ly.com' in request['url']):
        if 'apm' in request['url'] or 'log' in request['url'] or 'Trajectory' in request['url']:
            continue
        print(f"Index {i}: POST {request['url']}")
        response = entry['response']
        content = response.get('content', {}).get('text', '')
        if content:
            print(f"Resp: {content[:1000]}")
        print("-" * 50)
