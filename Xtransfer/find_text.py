import json
import sys

def find_entries_with_text(har_file, search_text):
    with open(har_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for entry in data['log']['entries']:
        url = entry['request']['url']
        req_body = entry['request'].get('postData', {}).get('text', '')
        resp_body = entry['response'].get('content', {}).get('text', '')
        
        if search_text in url or search_text in req_body or search_text in resp_body:
            print(f"URL: {url}")
            print(f"Method: {entry['request']['method']}")
            if search_text in req_body:
                print(f"Found in REQ: {req_body[:500]}...")
            if search_text in resp_body:
                print(f"Found in RESP: {resp_body[:500]}...")
            print("-" * 40)

if __name__ == "__main__":
    find_entries_with_text(sys.argv[1], sys.argv[2])
