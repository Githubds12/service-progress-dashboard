import json
import base64

def decode_341_res(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    res = har_data['log']['entries'][341]['response']['content']
    if 'text' in res:
        text = res['text']
        decoded = base64.b64decode(text)
        print("Decoded 341 Res:")
        print(decoded)
        print("-" * 50)
        import re
        strings = re.findall(b'[\x20-\x7E]{4,}', decoded)
        for s in strings:
            print(s.decode('ascii', errors='ignore'))

if __name__ == "__main__":
    decode_341_res('BPme.har')
