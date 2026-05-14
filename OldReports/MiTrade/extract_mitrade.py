import json
import os

har_path = r"c:\Users\Gorri\Documents\Reports\MiTrade\MiTrade.har"

with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

# 1. Find Package Name and Version
package_name = "Unknown"
version = "Unknown"

for entry in har_data['log']['entries']:
    # Check headers or post data for package info
    for header in entry['request']['headers']:
        if header['name'].lower() in ['user-agent', 'x-requested-with', 'package']:
            val = header['value']
            if "com." in val:
                package_name = val # Simplified check
            if "MiTrade/" in val:
                version = val.split("/")[-1]

    if 'postData' in entry['request'] and 'text' in entry['request']['postData']:
        text = entry['request']['postData']['text']
        if "package" in text.lower() or "version" in text.lower():
            # Try to extract from JSON if it is JSON
            try:
                data = json.loads(text)
                if 'packageName' in data: package_name = data['packageName']
                if 'version' in data: version = data['version']
            except:
                pass

print(f"Package: {package_name}")
print(f"Version: {version}")

# 2. Extract Auth Flow (POST requests)
output_path = r"c:\Users\Gorri\Documents\Reports\MiTrade\har_summary.txt"
keywords = ["otp", "login", "register", "verify", "phone", "sms", "send", "auth", "token"]

relevant_entries = []
for entry in har_data['log']['entries']:
    url = entry['request']['url']
    method = entry['request']['method']
    
    found = any(kw.lower() in url.lower() for kw in keywords)
    
    if not found and 'postData' in entry['request'] and 'text' in entry['request']['postData']:
        text = entry['request']['postData']['text']
        found = any(kw.lower() in text.lower() for kw in keywords)
        
    if found and method == "POST":
        relevant_entries.append({
            "method": method,
            "url": url,
            "status": entry['response']['status'],
            "request_body": entry['request'].get('postData', {}).get('text', ''),
            "response_body": entry['response'].get('content', {}).get('text', '')[:2000]
        })

with open(output_path, 'w', encoding='utf-8') as f:
    for i, entry in enumerate(relevant_entries):
        f.write(f"--- Entry {i+1} ---\n")
        f.write(f"URL: {entry['url']}\n")
        f.write(f"Method: {entry['method']}\n")
        f.write(f"Status: {entry['status']}\n")
        f.write(f"Request: {entry['request_body']}\n")
        f.write(f"Response: {entry['response_body']}\n\n")

print(f"Extracted {len(relevant_entries)} relevant entries to {output_path}")
