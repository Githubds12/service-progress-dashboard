import json

def find_success(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    entries = data['log']['entries']
    for entry in entries:
        resp_text = entry['response']['content'].get('text', '')
        if '"code":10001' in resp_text:
            print(f"SUCCESS URL: {entry['request']['url']}")
            # print(f"Response: {resp_text}")
            # print("-" * 50)

if __name__ == "__main__":
    find_success("Soul.har")
