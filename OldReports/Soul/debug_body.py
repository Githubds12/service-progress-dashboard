import json

with open("Soul.har", "r", encoding="utf-8") as f:
    data = json.load(f)

for entry in data['log']['entries']:
    if 'account/validate/register' in entry['request']['url']:
        if '"code":10001' in entry['response']['content'].get('text', ''):
            print("FOUND SUCCESSFUL REGISTER")
            print("PostData Keys:", entry['request'].get('postData', {}).keys())
            if 'postData' in entry['request']:
                print("Text Content:", entry['request']['postData'].get('text', 'EMPTY'))
                if 'params' in entry['request']['postData']:
                    print("Params:", entry['request']['postData']['params'])
