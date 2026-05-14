import json
import sys
from urllib.parse import urlparse

def extract_hosts(har_file):
    with open(har_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        hosts = set()
        for entry in data['log']['entries']:
            url = entry['request']['url']
            parsed = urlparse(url)
            hosts.add(parsed.netloc)
        for host in sorted(hosts):
            print(host)

if __name__ == "__main__":
    extract_hosts(sys.argv[1])
