import json
import sys

def extract_full_request(har_file, url_part):
    with open(har_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for entry in data['log']['entries']:
        url = entry['request']['url']
        if url_part in url:
            print(f"URL: {url}")
            print(f"Method: {entry['request']['method']}")
            print(f"Status: {entry['response']['status']}")
            
            resp_content = entry['response'].get('content', {})
            print(f"Resp Size: {resp_content.get('size')}")
            print(f"Resp MIME: {resp_content.get('mimeType')}")
            resp_text = resp_content.get('text', '')
            if resp_text:
                print(f"Response: {resp_text}")
            else:
                print("Response Body is Empty")
            print("-" * 80)

if __name__ == "__main__":
    extract_full_request(sys.argv[1], sys.argv[2])
