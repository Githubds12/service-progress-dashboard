import json
import base64

har_path = r"c:\Users\Gorri\Documents\Reports\GolfClash\GolfClash.har"
otp_str = "6197"
otp_bytes = otp_str.encode()
otp_int_le = (6197).to_bytes(2, 'little')
otp_int_be = (6197).to_bytes(2, 'big')

def search_binary(data_b64):
    try:
        data = base64.b64decode(data_b64)
        if otp_bytes in data: return "Found as String"
        if otp_int_le in data: return "Found as Int (LE)"
        if otp_int_be in data: return "Found as Int (BE)"
    except:
        pass
    return None

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    for i, entry in enumerate(entries):
        url = entry['request']['url']
        # Request body
        req_body = entry['request'].get('postData', {}).get('text', '')
        found = search_binary(req_body)
        if found:
            print(f"Index {i} Request: {url} - {found}")
            
        # Response body
        resp_body = entry['response'].get('content', {}).get('text', '')
        found = search_binary(resp_body)
        if found:
            print(f"Index {i} Response: {url} - {found}")
            
except Exception as e:
    print(f"Error: {e}")
