import json
har_path = r'c:\Users\Gorri\Documents\Reports\Deriv\Deriv.har'
with open(har_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
hosts = set()
for entry in data['log']['entries']:
    url = entry['request']['url']
    host = url.split('/')[2]
    hosts.add(host)
for h in sorted(hosts):
    print(h)
