import json
import base64
import gzip
import io

def search_grpc_decoded(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data['log']['entries']
    keywords = [b'profile', b'personal', b'phone', b'mobile', b'account']
    
    with open('grpc_search_results.txt', 'w', encoding='utf-8') as out:
        for i, entry in enumerate(entries):
            url = entry['request']['url']
            if 'bpglobal.com' in url:
                req_body = entry['request'].get('postData', {}).get('text', '')
                if req_body:
                    try:
                        decoded_req = base64.b64decode(req_body)
                        if decoded_req.startswith(b'\x1f\x8b'):
                            with gzip.GzipFile(fileobj=io.BytesIO(decoded_req)) as f_gzip:
                                decoded_req = f_gzip.read()
                        
                        if any(kw in decoded_req.lower() for kw in keywords):
                            out.write(f"--- ENTRY {i}: POST {url} ---\n")
                            out.write(f"Decoded Request Body contains keywords: {decoded_req}\n")
                            
                            # Also check response
                            res_content = entry['response'].get('content', {}).get('text', '')
                            if res_content:
                                try:
                                    decoded_res = base64.b64decode(res_content)
                                    if decoded_res.startswith(b'\x1f\x8b'):
                                        with gzip.GzipFile(fileobj=io.BytesIO(decoded_res)) as f_gzip:
                                            decoded_res = f_gzip.read()
                                    out.write(f"Decoded Response Body: {decoded_res}\n")
                                except:
                                    pass
                            out.write("-" * 50 + "\n\n")
                    except:
                        pass

if __name__ == "__main__":
    search_grpc_decoded('BPme.har')
