import json
import os

har_path = r"c:\Users\Gorri\Documents\Reports\NestleWaters\NestleWater.har"
output_path = r"c:\Users\Gorri\Documents\Reports\NestleWaters\har_summary.txt"

keywords = ["otp", "send", "verify", "phone", "mobile", "login", "register", "ciam", "auth"]

with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

relevant_entries = []
for entry in har_data['log']['entries']:
    url = entry['request']['url']
    method = entry['request']['method']
    
    # Check if any keyword is in the URL or request body
    found = any(kw.lower() in url.lower() for kw in keywords)
    
    if not found and 'postData' in entry['request'] and 'text' in entry['request']['postData']:
        text = entry['request']['postData']['text']
        found = any(kw.lower() in text.lower() for kw in keywords)
        
    if found:
        relevant_entries.append({
            "method": method,
            "url": url,
            "status": entry['response']['status'],
            "request_body": entry['request'].get('postData', {}).get('text', ''),
            "response_body": entry['response'].get('content', {}).get('text', '')[:1000] # Truncate response
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
