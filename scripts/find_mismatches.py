import json
import re
import os

# Paths
JS_FILE = r'c:\Users\Gorri\Documents\Reports\dashboard\apkhunter_data.js'

BRANDS = [
    'grab', 'tiktok', 'alibaba', 'uber', 'telegram', 'whatsapp', 'garena', 
    'shopee', 'facebook', 'instagram', 'microsoft', 'google', 'apple', 
    'amazon', 'netflix', 'steam', 'discord', 'viber', 'snapchat', 'tinder', 
    'binance', 'bybit', 'okx', 'kucoin', 'huobi', 'taobao', 'wechat', 'qq',
    'lazada', 'foodpanda', 'deliveroo', 'uber eats', 'bolt', 'lyft', 'gojek'
]

def find_mismatches():
    if not os.path.exists(JS_FILE):
        print(f"Error: {JS_FILE} not found")
        return

    with open(JS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Strip JS variable assignment
    json_str = re.sub(r'^window\.apkhunterData\s*=\s*', '', content.strip())
    json_str = re.sub(r';\s*$', '', json_str)
    
    try:
        data = json.loads(json_str)
    except Exception as e:
        print(f"JSON Parse Error: {e}")
        return

    mismatches = []
    
    for item in data:
        name = item.get('name', '').lower()
        sms = item.get('sms', '').lower()
        if not sms:
            continue
            
        found_brands = [b for b in BRANDS if b in sms]
        
        # If we find a brand in the message that isn't the service name
        # e.g. name is "notice" and message contains "grab"
        for brand in found_brands:
            if brand not in name:
                mismatches.append({
                    'id': item['id'],
                    'name': item['name'],
                    'brand_found': brand,
                    'sms': item['sms']
                })
                break # Only need one mismatch per service to flag it

    print(f"{'SERVICE':<15} | {'BRAND IN SMS':<15} | {'SAMPLE SMS'}")
    print("-" * 80)
    for m in mismatches[:100]: # Increase limit
        try:
            sms_preview = m['sms'].replace('\n', ' ')[:80]
            print(f"{m['name']:<15} | {m['brand_found']:<15} | {sms_preview}")
        except:
            # Fallback for unicode issues
            safe_sms = m['sms'].encode('ascii', 'ignore').decode().replace('\n', ' ')[:80]
            print(f"{m['name']:<15} | {m['brand_found']:<15} | {safe_sms}")

    print(f"\nTotal potential rotatory services found: {len(mismatches)}")

if __name__ == "__main__":
    find_mismatches()
