import json

def dump_auth_requests(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data['log']['entries']
    for i, entry in enumerate(entries):
        url = entry['request']['url']
        if '/authenticate' in url and entry['request']['method'] == 'POST':
            print(f"--- ENTRY {i} ---")
            print(f"URL: {url}")
            print(f"Request: {entry['request'].get('postData', {}).get('text', '')}")
            print("-" * 50)

if __name__ == "__main__":
    dump_auth_requests('BPme.har')
