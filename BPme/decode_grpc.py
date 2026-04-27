import json
import base64
import gzip
import io

def decode_grpc(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data['log']['entries']
    
    with open('grpc_decoded.txt', 'w', encoding='utf-8') as out:
        for i, entry in enumerate(entries):
            url = entry['request']['url']
            if 'bpglobal.com' in url:
                out.write(f"--- ENTRY {i}: {entry['request']['method']} {url} ---\n")
                
                # Try to decode request body
                req_body = entry['request'].get('postData', {}).get('text', '')
                if req_body:
                    try:
                        # Check if it looks like base64
                        decoded_req = base64.b64decode(req_body)
                        # Check if it's gzip'd
                        if decoded_req.startswith(b'\x1f\x8b'):
                            with gzip.GzipFile(fileobj=io.BytesIO(decoded_req)) as f_gzip:
                                decompressed = f_gzip.read()
                                out.write(f"Decoded/Decompressed Request Body: {decompressed}\n")
                        else:
                            out.write(f"Decoded Request Body: {decoded_req}\n")
                    except:
                        out.write(f"Raw Request Body: {req_body[:500]}...\n")
                
                # Try to decode response body
                res_content = entry['response'].get('content', {}).get('text', '')
                if res_content:
                    try:
                        decoded_res = base64.b64decode(res_content)
                        if decoded_res.startswith(b'\x1f\x8b'):
                            with gzip.GzipFile(fileobj=io.BytesIO(decoded_res)) as f_gzip:
                                decompressed = f_gzip.read()
                                out.write(f"Decoded/Decompressed Response Body: {decompressed}\n")
                        else:
                            out.write(f"Decoded Response Body: {decoded_res}\n")
                    except:
                        out.write(f"Raw Response Body: {res_content[:500]}...\n")
                
                out.write("-" * 50 + "\n\n")

if __name__ == "__main__":
    decode_grpc('BPme.har')
