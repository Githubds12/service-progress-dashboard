import json
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

har_path = r'c:\Users\Gorri\Documents\Reports\BetLabel\BetLabel.har'

with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for i, entry in enumerate(data['log']['entries']):
    if '92617' in str(entry) or 'verify' in entry['request']['url'].lower() or 'check' in entry['request']['url'].lower():
        request = entry['request']
        print(f"Index: {i}")
        print(f"URL: {request['url']}")
        if 'postData' in request:
            print(f"Body: {request['postData'].get('text', 'No text content')}")
        print("-" * 50)
