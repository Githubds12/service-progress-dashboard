import json

def extract_callback_inputs(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data['log']['entries']
    for i, entry in enumerate(entries):
        url = entry['request']['url']
        if '/authenticate' in url and entry['request']['method'] == 'POST':
            req_body = entry['request'].get('postData', {}).get('text', '')
            if req_body:
                try:
                    data = json.loads(req_body)
                    for cb in data.get('callbacks', []):
                        for inp in cb.get('input', []):
                            print(f"--- ENTRY {i} ---")
                            print(f"Input Name: {inp.get('name')}")
                            print(f"Input Value: {inp.get('value')}")
                except:
                    pass

if __name__ == "__main__":
    extract_callback_inputs('BPme.har')
