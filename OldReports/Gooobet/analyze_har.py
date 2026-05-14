import json
import sys
import io

# Set stdout to UTF-8 to handle special characters
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def analyze_har(har_path):
    with open(har_path, 'r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)
    
    entries = data.get('log', {}).get('entries', [])
    print(f"Total entries: {len(entries)}")
    
    keywords = ['sms', 'verify', 'auth', 'login', 'register', 'code', 'otp', 'phone', 'mobile']
    
    for entry in entries:
        request = entry.get('request', {})
        url = request.get('url', '')
        method = request.get('method', '')
        
        # Look for registration, phone, sms, or verify endpoints
        relevant_keywords = ['register', 'phone', 'sms', 'verify', 'otp', 'code', 'auth', 'captcha']
        if method == 'POST' or any(k in url.lower() for k in relevant_keywords):
            # Skip noise like firebase, analytics, etc.
            if any(noise in url.lower() for noise in ['firebase', 'google-analytics', 'facebook', 'crashlytics', 'adjust', 'event.json']):
                continue
                
            print(f"\nURL: {url}")
            print(f"Method: {method}")
            
            headers = {h['name']: h['value'] for h in request.get('headers', [])}
            # Only print relevant headers
            rel_headers = ['User-Agent', 'Content-Type', 'X-Requested-With', 'Authorization', 'X-App-Id']
            print(f"Headers: {json.dumps({k: v for k, v in headers.items() if any(rh in k for rh in rel_headers)}, indent=2)}")
            
            post_data = request.get('postData', {}).get('text', 'No body')
            print(f"Request Body: {post_data}")
            
            response = entry.get('response', {})
            response_body = response.get('content', {}).get('text', 'No body')
            print(f"Response Body: {response_body[:1000]}...")
            print("-" * 40)

if __name__ == "__main__":
    analyze_har(sys.argv[1])
