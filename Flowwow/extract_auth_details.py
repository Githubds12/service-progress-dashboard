import json

har_file = r'c:\Users\Gorri\Documents\Reports\Flowwow\Flowwow.har'

with open(har_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data['log']['entries']

target_indices = [51, 53]

for i in target_indices:
    entry = entries[i]
    request = entry['request']
    url = request['url']
    method = request['method']
    
    print(f"[{i}] {method} {url}")
    print("Headers:")
    for header in request['headers']:
        print(f"  {header['name']}: {header['value']}")
    
    if 'postData' in request and 'text' in request['postData']:
        print(f"Request body: {request['postData']['text']}")
    
    response = entry['response']
    print(f"Response status: {response['status']}")
    print("Response Headers:")
    for header in response['headers']:
        print(f"  {header['name']}: {header['value']}")
    if 'content' in response and 'text' in response['content']:
        print(f"Response body: {response['content']['text']}")
    print("-" * 50)
