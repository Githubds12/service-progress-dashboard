import json
import os

har_path = r"c:\Users\Gorri\Documents\Reports\NestleWaters\NestleWater.har"
output_path = r"c:\Users\Gorri\Documents\Reports\NestleWaters\har_all_posts.txt"

with open(har_path, 'r', encoding='utf-8') as f:
    har_data = json.load(f)

relevant_entries = []
for entry in har_data['log']['entries']:
    url = entry['request']['url']
    method = entry['request']['method']
    
    if method == "POST" and ("nestle" in url.lower()):
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

print(f"Extracted {len(relevant_entries)} POST entries to {output_path}")
