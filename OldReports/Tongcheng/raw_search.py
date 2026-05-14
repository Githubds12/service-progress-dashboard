import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

har_path = r'c:\Users\Gorri\Documents\Reports\Tongcheng\Tongcheng.har'

with open(har_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = '您输入的验证码有误'
index = content.find(target)
if index != -1:
    print(f"Found at {index}")
    print(content[max(0, index-1000):index+1000])
else:
    # Try searching for the unicode escaped version
    target = "\\u60a8\\u8f93\\u5165\\u7684\\u9a8c\\u8bc1\\u7801\\u6709\\u8bef"
    index = content.find(target)
    if index != -1:
        print(f"Found escaped at {index}")
        print(content[max(0, index-1000):index+1000])
    else:
        print("Not found")
