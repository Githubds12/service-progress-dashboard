import json
import re

har_path = r"c:\Users\Gorri\Documents\Reports\Yamaha\Yamaha.har"

with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

for entry in har_data['log']['entries']:
    url = entry['request']['url']
    if "c377768625-eu.com" in url:
        for header in entry['request']['headers']:
            if "version" in header['name'].lower():
                print(f"Header {header['name']}: {header['value']}")
        if 'postData' in entry['request'] and 'text' in entry['request']['postData']:
             text = entry['request']['postData']['text']
             if "version" in text.lower():
                 print(f"Body: {text}")
