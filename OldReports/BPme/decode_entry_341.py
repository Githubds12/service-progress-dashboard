import json
import base64
import gzip
import io

def decode_entry(har_file, index):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entry = har_data['log']['entries'][index]
    req_body = entry['request'].get('postData', {}).get('text', '')
    if req_body:
        try:
            decoded = base64.b64decode(req_body)
            if decoded.startswith(b'\x1f\x8b'):
                with gzip.GzipFile(fileobj=io.BytesIO(decoded)) as f_gzip:
                    decoded = f_gzip.read()
            print(f"ENTRY {index} Decoded Req: {decoded}")
        except:
            print(f"ENTRY {index} Raw Req: {req_body}")
            
    res_content = entry['response'].get('content', {}).get('text', '')
    if res_content:
        try:
            decoded = base64.b64decode(res_content)
            if decoded.startswith(b'\x1f\x8b'):
                with gzip.GzipFile(fileobj=io.BytesIO(decoded)) as f_gzip:
                    decoded = f_gzip.read()
            print(f"ENTRY {index} Decoded Res: {decoded}")
        except:
            print(f"ENTRY {index} Raw Res: {res_content}")

if __name__ == "__main__":
    decode_entry('BPme.har', 341)
