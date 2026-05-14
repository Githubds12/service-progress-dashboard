import json
import sys

def extract_headers(har_file, url_part):
    with open(har_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for entry in data['log']['entries']:
        url = entry['request']['url']
        if url_part in url:
            print(f"URL: {url}")
            print("Response Headers:")
            for h in entry['response']['headers']:
                print(f"  {h['name']}: {h['value']}")
            print("-" * 80)

if __name__ == "__main__":
    extract_headers(sys.argv[1], sys.argv[2])
