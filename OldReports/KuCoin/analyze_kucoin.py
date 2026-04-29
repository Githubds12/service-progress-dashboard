import json
import sys
import os
import re

har_path = 'KuCoin/KuCoin.har'
with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

entries = har_data['log']['entries']
print(f"Total entries: {len(entries)}")

# 1. Package Name & Version Extraction
package_name = "Unknown"
app_version = "Unknown"
for entry in entries:
    ua = next((h['value'] for h in entry['request']['headers'] if h['name'].lower() == 'user-agent'), "")
    pkg_match = re.search(r'([a-z0-9]+\.[a-z0-9]+\.[a-z0-9]+)', ua)
    if pkg_match and 'mozilla' not in ua.lower():
        package_name = pkg_match.group(1)
    
    version_header = next((h['value'] for h in entry['request']['headers'] if 'version' in h['name'].lower()), None)
    if version_header:
        app_version = version_header
        
print(f"Package Name: {package_name}")
print(f"App Version: {app_version}")

# 2. Key API Search
keywords = ['register', 'login', 'otp', 'verify', 'code', 'signup', 'auth', 'sms', 'check']
unique_endpoints = set()

for entry in entries:
    url = entry['request']['url']
    method = entry['request']['method']
    status = entry['response']['status']
    
    endpoint = f"{method} {url.split('?')[0]}"
    if endpoint not in unique_endpoints:
        unique_endpoints.add(endpoint)
        
    if any(kw in url.lower() for kw in keywords):
        print(f"[{method}] {status} - {url}")
        if 'postData' in entry['request']:
            print(f"  PostData: {entry['request']['postData'].get('text', 'N/A')[:500]}")
        print("-" * 50)

print("\n--- Unique Endpoints ---")
for ep in sorted(list(unique_endpoints)):
    print(ep)
