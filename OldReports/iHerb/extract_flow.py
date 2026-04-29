import json
import sys

har_path = 'iHerb/iHerb.har'
with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

for entry in har_data['log']['entries']:
    url = entry['request']['url']
    if '/auth/api/otp/send' in url or '/auth/api/otp/validate' in url or '/auth/api/register' in url:
        print(f"URL: {url}")
        print(f"Method: {entry['request']['method']}")
        if 'postData' in entry['request']:
            print(f"Request Body: {entry['request']['postData'].get('text', 'N/A')}")
        print(f"Response Status: {entry['response']['status']}")
        if 'text' in entry['response']['content']:
            print(f"Response Body: {entry['response']['content']['text'][:500]}")
        print("-" * 50)
