import json
import re

def find_all_auth_indexes(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    indexes = set()
    for entry in har_data['log']['entries']:
        url = entry['request']['url']
        match = re.search(r'authIndexValue=([^&\"\' ]+)', url)
        if match:
            indexes.add(match.group(1))
    
    print("Found Auth Indexes:", indexes)

if __name__ == "__main__":
    find_all_auth_indexes('BPme.har')
