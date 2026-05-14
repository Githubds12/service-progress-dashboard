import json
import base64

def hex_dump_entry(har_file, index):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entry = har_data['log']['entries'][index]
    req_body = entry['request'].get('postData', {}).get('text', '')
    if req_body:
        try:
            decoded = base64.b64decode(req_body)
            print(f"ENTRY {index} Hex Dump:")
            print(decoded.hex(' '))
            print("-" * 50)
            print(f"ASCII Dump:")
            print(''.join(chr(b) if 32 <= b <= 126 else '.' for b in decoded))
        except:
            print(f"ENTRY {index} Raw: {req_body}")

if __name__ == "__main__":
    hex_dump_entry('BPme.har', 341)
