import json
import base64

har_path = r"c:\Users\Gorri\Documents\Reports\GolfClash\GolfClash.har"
idx = 418

try:
    with open(har_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entry = har_data['log']['entries'][idx]
    post_data = entry['request'].get('postData', {})
    text = post_data.get('text', '')
    
    with open('req_418_raw.bin', 'wb') as f:
        try:
            f.write(base64.b64decode(text))
            print("Wrote decoded base64 to req_418_raw.bin")
        except:
            f.write(text.encode())
            print("Wrote raw text to req_418_raw.bin")
            
    # Also do the response
    resp_data = entry['response'].get('content', {})
    text = resp_data.get('text', '')
    with open('resp_418_raw.bin', 'wb') as f:
        try:
            f.write(base64.b64decode(text))
            print("Wrote decoded base64 to resp_418_raw.bin")
        except:
            f.write(text.encode())
            print("Wrote raw text to resp_418_raw.bin")

except Exception as e:
    print(f"Error: {e}")
