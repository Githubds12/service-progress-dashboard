import json

def list_patch_put(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    for i, entry in enumerate(har_data['log']['entries']):
        method = entry['request']['method']
        if method in ['PATCH', 'PUT']:
            print(f"{i}: {method} {entry['request']['url']}")

if __name__ == "__main__":
    list_patch_put('BPme.har')
