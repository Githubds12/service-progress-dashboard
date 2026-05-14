import json

def list_phone_entries(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    for i, entry in enumerate(har_data['log']['entries']):
        if 'phone' in str(entry).lower():
            print(f"{i}: {entry['request']['method']} {entry['request']['url']}")

if __name__ == "__main__":
    list_phone_entries('BPme.har')
