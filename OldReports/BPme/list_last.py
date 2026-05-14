import json

def list_last_entries(har_file, count=100):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    total = len(har_data['log']['entries'])
    for i, entry in enumerate(har_data['log']['entries'][-count:]):
        print(f"{total-count+i}: {entry['request']['method']} {entry['request']['url']}")

if __name__ == "__main__":
    list_last_entries('BPme.har')
