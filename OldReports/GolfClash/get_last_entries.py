import json
import base64

har_path = r"c:\Users\Gorri\Documents\Reports\GolfClash\GolfClash.har"

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    last_entries = entries[-10:]
    
    print(f"Total entries: {len(entries)}")
    print("--- Last 10 Entries ---")
    for i, entry in enumerate(last_entries):
        idx = len(entries) - 10 + i
        req = entry['request']
        resp = entry['response']
        print(f"Index: {idx}")
        print(f"URL: {req['url']}")
        print(f"Method: {req['method']}")
        print(f"Status: {resp['status']}")
        
        post_data = req.get('postData', {}).get('text', 'N/A')
        resp_text = resp.get('content', {}).get('text', 'N/A')
        
        # Check if it's base64 or hex
        print(f"Request Body: {post_data[:100]}...")
        print(f"Response Body: {resp_text[:100]}...")
        
        # Try decoding if it looks like base64
        try:
            decoded_req = base64.b64decode(post_data)
            print(f"Decoded Req (printable): {''.join(chr(b) if 32 <= b <= 126 else '.' for b in decoded_req)[:100]}")
        except:
            pass
            
        print("-" * 20)
        
except Exception as e:
    print(f"Error: {e}")
