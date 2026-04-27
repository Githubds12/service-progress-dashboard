import json
import re

def find_endpoints(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data['log']['entries']
    relevant_keywords = ['phone', 'mobile', 'otp', 'verify', 'profile', 'personal', 'settings']
    
    for entry in entries:
        req = entry['request']
        url = req['url']
        method = req['method']
        
        # Check URL or body for keywords
        found = False
        if any(kw in url.lower() for kw in relevant_keywords):
            found = True
        
        post_data = req.get('postData', {}).get('text', '')
        if post_data and any(kw in post_data.lower() for kw in relevant_keywords):
            found = True
            
        if found:
            print(f"--- {method} {url} ---")
            print("Request Body:", post_data[:500])
            res_content = entry['response'].get('content', {}).get('text', '')
            print("Response Body:", res_content[:500])
            print("\n")

if __name__ == "__main__":
    find_endpoints('BPme.har')
