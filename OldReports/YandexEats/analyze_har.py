import json
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

har_path = r'c:\Users\Gorri\Documents\Reports\YandexEats\YandexEats.har'

with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for i in range(120, 160):
    if i < len(data['log']['entries']):
        entry = data['log']['entries'][i]
        request = entry['request']
        print(f"Index: {i}")
        print(f"URL: {request['url']}")
        if 'postData' in request:
            print(f"Body: {request['postData'].get('text', 'No text content')}")
        print("-" * 50)
