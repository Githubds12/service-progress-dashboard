import json
import sys

har_path = 'KuCoin/KuCoin.har'
with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

for entry in har_data['log']['entries']:
    url = entry['request']['url']
    if any(p in url for p in ['/auth/check-user-account', '/auth/captcha-validation', '/auth/validation-code', '/auth/verify-validation-code', '/auth/sign-up']):
        print(f"URL: {url}")
        print(f"Method: {entry['request']['method']}")
        if 'postData' in entry['request']:
            print(f"Request Body: {entry['request']['postData'].get('text', 'N/A')}")
        print(f"Response Status: {entry['response']['status']}")
        if 'text' in entry['response']['content']:
            print(f"Response Body: {entry['response']['content']['text'][:500]}")
        print("-" * 50)
