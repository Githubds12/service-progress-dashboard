import json

har_path = r"c:\Users\Gorri\Documents\Reports\Yamaha\Yamaha.har"

with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

for entry in har_data['log']['entries']:
    if 'postData' in entry['request'] and 'text' in entry['request']['postData']:
        text = entry['request']['postData']['text']
        if "app_version" in text:
            print(text)
            break
