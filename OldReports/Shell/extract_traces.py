import json

har_path = r'c:\Users\Gorri\Documents\Reports\Shell\Shell.har'

with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data['log']['entries']

for entry in entries:
    url = entry['request']['url']
    if 'auth/v1/otp/generate' in url:
        print("--- OTP GENERATE ---")
        print(f"URL: {url}")
        print("Headers:")
        for h in entry['request']['headers']:
            print(f"  {h['name']}: {h['value']}")
        print(f"Body: {entry['request'].get('postData', {}).get('text', 'N/A')}")
        print("Response Headers:")
        for h in entry['response']['headers']:
            print(f"  {h['name']}: {h['value']}")
        print(f"Response Body: {entry['response'].get('content', {}).get('text', 'N/A')}")
        print("-" * 50)
    elif 'auth/v1/otp/validate' in url:
        print("--- OTP VALIDATE ---")
        print(f"URL: {url}")
        print("Headers:")
        for h in entry['request']['headers']:
            print(f"  {h['name']}: {h['value']}")
        print(f"Body: {entry['request'].get('postData', {}).get('text', 'N/A')}")
        print("Response Headers:")
        for h in entry['response']['headers']:
            print(f"  {h['name']}: {h['value']}")
        print(f"Response Body: {entry['response'].get('content', {}).get('text', 'N/A')}")
        print("-" * 50)
