import json
import sys
import os

har_path = sys.argv[1]
with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

entries = har_data['log']['entries']
print(f"Total entries: {len(entries)}")

# Search for relevant keywords
keywords = ['register', 'otp', 'code', 'prescription', 'redeem', 'phone', 'login', 'account', 'erx', 'recipe', 'mfa', 'verify']

unique_endpoints = set()

for entry in entries:
    url = entry['request']['url']
    method = entry['request']['method']
    status = entry['response']['status']
    
    endpoint = f"{method} {url.split('?')[0]}"
    if endpoint not in unique_endpoints:
        unique_endpoints.add(endpoint)
        
    if any(kw in url.lower() for kw in keywords):
        print(f"### Endpoint: {method} {url}")
        print(f"**Status**: {status}")
        
        # Request
        print("#### Request")
        if 'postData' in entry['request']:
            print("```json")
            print(entry['request']['postData'].get('text', 'N/A'))
            print("```")
        else:
            print("*No Body*")
            
        # Response
        print("#### Response")
        content = entry['response']['content']
        if 'text' in content:
            print("```json")
            # Try to pretty print if it's JSON
            try:
                data = json.loads(content['text'])
                print(json.dumps(data, indent=2))
            except:
                print(content['text'][:2000]) # Fallback to raw text
            print("```")
        else:
            print("*No Body*")
        print("\n" + "="*80 + "\n")

print("\n--- Unique Endpoints ---")
for ep in sorted(list(unique_endpoints)):
    print(ep)
