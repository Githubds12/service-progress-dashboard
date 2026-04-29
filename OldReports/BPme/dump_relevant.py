import json

def dump_relevant(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data['log']['entries']
    relevant_keywords = ['phone', 'mobile', 'otp', 'verify', 'personal', 'settings', 'account']
    
    with open('relevant_dump.txt', 'w', encoding='utf-8') as out:
        for i, entry in enumerate(entries):
            req = entry['request']
            url = req['url']
            post_data = req.get('postData', {}).get('text', '')
            res_content = entry['response'].get('content', {}).get('text', '')
            
            combined = (url + post_data + res_content).lower()
            if any(kw in combined for kw in relevant_keywords):
                out.write(f"--- ENTRY {i}: {req['method']} {url} ---\n")
                out.write(f"Headers: {json.dumps(req['headers'], indent=2)}\n")
                out.write(f"Request Body: {post_data}\n")
                out.write(f"Response Body: {res_content}\n")
                out.write("=" * 50 + "\n\n")

if __name__ == "__main__":
    dump_relevant('BPme.har')
