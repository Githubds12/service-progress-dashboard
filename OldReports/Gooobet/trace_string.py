import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def find_string(har_path, search_str):
    with open(har_path, 'r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)
    
    entries = data.get('log', {}).get('entries', [])
    
    for entry in entries:
        request = entry.get('request', {})
        response = entry.get('response', {})
        
        req_body = request.get('postData', {}).get('text', '')
        resp_body = response.get('content', {}).get('text', '')
        
        if 'hd-api/verify' in request.get('url'):
            print(f"\nURL: {request.get('url')}")
            print(f"Method: {request.get('method')}")
            print(f"Request Body: {req_body}")
            print(f"Response Body: {resp_body}")
            print("-" * 20)

if __name__ == "__main__":
    find_string(sys.argv[1], sys.argv[2])
