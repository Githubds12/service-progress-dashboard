import json
import sys

def extract_auth_flow(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    auth_domains = ['xtransfer.com', 'geetest.com']
    
    # Set console encoding to utf-8
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    for entry in data['log']['entries']:
        url = entry['request']['url']
        if any(domain in url for domain in auth_domains):
            # Skip noise
            if any(x in url for x in ['hotupdate', 'femonitorapi', 'static', 'Announcement', 'album']):
                continue
                
            method = entry['request']['method']
            status = entry['response']['status']
            print(f"[{method}] {status} - {url}")
            
            # Print body snippets if POST
            if method == 'POST':
                post_data = entry['request'].get('postData', {})
                text = post_data.get('text', '')
                if text:
                    print(f"  Req Body: {text[:500]}...")
            
            # Print response body snippets
            content = entry['response'].get('content', {})
            resp_text = content.get('text', '')
            if resp_text:
                print(f"  Resp Body: {resp_text[:500]}...")
            print("-" * 40)

if __name__ == "__main__":
    extract_auth_flow(sys.argv[1])
