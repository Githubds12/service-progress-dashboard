import json

def list_urls(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data['log']['entries']
    for i, entry in enumerate(entries):
        req = entry['request']
        url = req['url']
        method = req['method']
        print(f"{i}: {method} {url}")

if __name__ == "__main__":
    list_urls('BPme.har')
