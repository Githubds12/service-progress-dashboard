import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def analyze_har(har_path):
    with open(har_path, 'r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)
    
    entries = data.get('log', {}).get('entries', [])
    
    for entry in entries:
        url = entry.get('request', {}).get('url', '')
        if 'hd-api/verify' in url:
            print(f"\nURL: {url}")
            print(f"Method: {entry['request']['method']}")
            headers = {h['name']: h['value'] for h in entry['request'].get('headers', [])}
            print(f"Headers: {json.dumps(headers, indent=2)}")
            
            response_body = entry['response'].get('content', {}).get('text', 'No body')
            print(f"Response Body: {response_body[:500]}...")

if __name__ == "__main__":
    analyze_har(sys.argv[1])
