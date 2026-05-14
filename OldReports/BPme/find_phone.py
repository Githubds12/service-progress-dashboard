import json

def find_phone_flows(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    entries = har_data['log']['entries']
    
    with open('phone_flows.txt', 'w', encoding='utf-8') as out:
        for i, entry in enumerate(entries):
            req = entry['request']
            url = req['url']
            post_data = req.get('postData', {}).get('text', '')
            res_content = entry['response'].get('content', {}).get('text', '')
            
            if '+48' in post_data or '+48' in url:
                out.write(f"--- ENTRY {i}: {req['method']} {url} ---\n")
                out.write(f"Request Body: {post_data}\n")
                out.write(f"Response Body: {res_content}\n")
                out.write("-" * 30 + "\n")

if __name__ == "__main__":
    find_phone_flows('BPme.har')
