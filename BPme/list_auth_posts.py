import json

def list_auth_posts(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    for i, entry in enumerate(har_data['log']['entries']):
        url = entry['request']['url']
        if '/authenticate' in url and entry['request']['method'] == 'POST':
            print(f"{i}: {url}")

if __name__ == "__main__":
    list_auth_posts('BPme.har')
