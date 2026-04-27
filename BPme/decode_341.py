import json
import base64

def decode_341(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    text = har_data['log']['entries'][341]['request']['_content']['text']
    decoded = base64.b64decode(text)
    print("Decoded 341:")
    print(decoded)
    print("-" * 50)
    # Search for strings
    import re
    strings = re.findall(b'[\x20-\x7E]{4,}', decoded)
    for s in strings:
        print(s.decode('ascii', errors='ignore'))

if __name__ == "__main__":
    decode_341('BPme.har')
