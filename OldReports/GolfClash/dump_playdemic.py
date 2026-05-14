import json
import base64

har_path = r"c:\Users\Gorri\Documents\Reports\GolfClash\GolfClash.har"

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data.get("log", {}).get("entries", [])
    for i, entry in enumerate(entries):
        url = entry['request']['url']
        if 'playdemic.com' in url:
            post_data = entry['request'].get('postData', {}).get('text', '')
            if post_data:
                print(f"--- Entry {i}: {url} ---")
                try:
                    # Try to see if it's base64 encoded by HTTP Toolkit
                    decoded = base64.b64decode(post_data)
                    print(f"Decoded (hex): {decoded.hex()[:100]}")
                    print(f"Decoded (printable): {''.join(chr(b) if 32 <= b <= 126 else '.' for b in decoded)[:100]}")
                except:
                    print(f"Raw: {post_data[:100]}")
except Exception as e:
    print(f"Error: {e}")
