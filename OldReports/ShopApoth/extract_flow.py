import json
import sys

def extract():
    with open('ShopApoth/ShopApoth.har', 'r', encoding='utf-8') as f:
        har = json.load(f)
    
    entries = har['log']['entries']
    relevant_urls = [
        'auth/v2/com/register',
        'customer/v1/com/mfa',
        'nfc-health-card-position/api/v1/nfc-position',
        'session/v1/com/erx-session-status'
    ]
    
    report = "# Shop Apotheke API Request/Response Logs\n\n"
    
    for entry in entries:
        url = entry['request']['url']
        method = entry['request']['method']
        if any(r in url for r in relevant_urls):
            status = entry['response']['status']
            report += f"### {method} {url}\n"
            report += f"**Status**: {status}\n\n"
            
            report += "#### Request\n"
            if 'postData' in entry['request']:
                report += "```json\n"
                try:
                    req_data = json.loads(entry['request']['postData']['text'])
                    report += json.dumps(req_data, indent=2)
                except:
                    report += entry['request']['postData'].get('text', 'N/A')
                report += "\n```\n\n"
            else:
                report += "*No Body*\n\n"
                
            report += "#### Response\n"
            content = entry['response']['content']
            if 'text' in content:
                report += "```json\n"
                try:
                    res_data = json.loads(content['text'])
                    report += json.dumps(res_data, indent=2)
                except:
                    report += content['text'][:1000]
                report += "\n```\n\n"
            else:
                report += "*No Body*\n\n"
            report += "---\n\n"
            
    with open('ShopApoth/flow_logs.md', 'w', encoding='utf-8') as f:
        f.write(report)

if __name__ == "__main__":
    extract()
