import json

def extract_authenticate_flow(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data['log']['entries']
    
    with open('authenticate_flow.txt', 'w', encoding='utf-8') as out:
        for i, entry in enumerate(entries):
            req = entry['request']
            url = req['url']
            if '/authenticate' in url and req['method'] == 'POST':
                out.write(f"--- ENTRY {i}: POST {url} ---\n")
                post_data = req.get('postData', {}).get('text', '')
                out.write(f"Request Body: {post_data}\n")
                res_content = entry['response'].get('content', {}).get('text', '')
                out.write(f"Response Body: {res_content}\n")
                out.write("=" * 50 + "\n\n")

if __name__ == "__main__":
    extract_authenticate_flow('BPme.har')
