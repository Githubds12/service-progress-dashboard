import json
import csv
import os
import requests
import time
import re
from datetime import datetime

# --- CONFIGURATION ---
DB_PATH = r"C:\HTB-Notes-Portal\apk_local_database.json"
CSV_PATH = r"C:\HTB-Notes-Portal\fresh_detailed.csv"
OUTPUT_JS = r"c:\Users\Gorri\Documents\Reports\dashboard\apkhunter_data.js"

# API Configuration (from api_portal.py)
API_BASE = "http://51.195.24.179:8092/api"
EMAIL = "deepanshu@test.com"
PASS = "deep@nshu"

# Pre-defined high-intel targets (manual verified)
SECURITY_INTEL = {
    "sms20120": 100, # Bank of America
    "sms10220": 45,  # Telegram
    "sms30550": 90,  # Crypto.com
}

TIER_MAP = {
    "Tier 1 (Instant/Public)": "Easy (Public Flow)",
    "Tier 2 (Moderate/Private)": "Moderate (Auth Required)",
    "Tier 3 (Hard/Secured)": "Hard (App Only/Pinning)"
}

def fetch_api_claimed_ids():
    """Fetches unique claimed service IDs from the external API projects."""
    try:
        print("[*] API: Logging in to fetch claimed services...")
        res = requests.post(f"{API_BASE}/auth/login", json={"email": EMAIL, "password": PASS}, timeout=5)
        if res.status_code != 200:
            print(f"[-] API: Login failed ({res.status_code})")
            return set()
        
        token = res.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        print("[*] API: Fetching projects to determine claimed status...")
        res = requests.get(f"{API_BASE}/projects", headers=headers, timeout=10)
        if res.status_code != 200:
            print(f"[-] API: Failed to fetch projects ({res.status_code})")
            return set()
            
        projects = res.json()
        claimed_ids = set()
        if isinstance(projects, list):
            for p in projects:
                if isinstance(p, dict) and p.get('linked_service_id'):
                    claimed_ids.add(p.get('linked_service_id'))
        
        print(f"[+] API: Found {len(claimed_ids)} claimed services via portal projects.")
        return claimed_ids
    except Exception as e:
        print(f"[-] API: Error during sync: {e}")
        return set()

def sync():
    print("[*] Starting APKHunter Sync...")
    
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found")
        return

    # Load API Claims
    api_claims = fetch_api_claimed_ids()

    # Load Local Claims/Notes/Root/NF
    claims_dict = {}
    notes_dict = {}
    root_dict = {}
    nf_dict = {}
    updated_dict = {}
    if os.path.exists(DB_PATH):
        with open(DB_PATH, 'r') as f:
            db = json.load(f)
            claims_dict = db.get('claimed', {})
            notes_dict = db.get('notes', {})
            root_dict = db.get('root_detected', {})
            nf_dict = db.get('not_found', {})
            updated_dict = db.get('last_updated', {})
            print(f"[+] Loaded {len(claims_dict)} claims, {len(notes_dict)} notes from local DB.")

    final_data = []
    
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tid = row.get("API_ID", row.get("Slug", "")).strip().lower()
            if not tid: continue
            
            name = row.get("Name", tid)
            tier = row.get("Category", row.get("Tier", "Tier 2 (Moderate/Private)"))
            base_score = 50
            
            p_issues = []
            note = notes_dict.get(tid, "")
            
            # Merged Claimed Logic: Local DB OR External API
            local_claimed = claims_dict.get(tid, False)
            is_api_claimed = tid in api_claims
            claimed = local_claimed or is_api_claimed
            
            if is_api_claimed and not local_claimed:
                if not note:
                    note = "[Portal] Service claimed in Intelligence Portal."
                else:
                    note = f"{note} (Also claimed in Portal)".strip()
            
            intel_pool = (" ".join([str(x.get('text','')).lower() for x in p_issues]) + " " + note.lower()).strip()
            
            # --- ELITE CATEGORIZATION ENGINE ---
            def guess_category(name, tid, desc="", sms=""):
                # Clean name: remove common domains and suffixes
                clean_name = name.lower()
                for suffix in ['.com', '.ru', '.net', '.org', '.info', '.de', '.in', '.uk', '.ae', '.eg', '.vn', '.cn', '.tr']:
                    clean_name = clean_name.replace(suffix, '')
                
                # Combine all searchable text
                n = (clean_name + " " + name.lower() + " " + tid.lower() + " " + desc.lower() + " " + (sms or "").lower())
                n = re.sub(r'[^a-z0-9]', ' ', n) # Replace all non-alphanumeric with spaces
                
                cat_map = {
                    "Banking/Fintech": ['bank', 'pay', 'wallet', 'finance', 'invest', 'crypto', 'coin', 'trading', 'broker', 'card', 'loan', 'credit', 'money', 'cash', 'transfer', 'ledger', 'stock', 'forex', 'capital', 'wealth', 'save', 'budget', 'billing', 'invoice', 'checkout', 'pos', 'payment', 'atm', 'remit', 'paisa', 'khata', 'upi', 'fintech', 'merchant', 'mortgage', 'insurance', 'repay', 'interest', 'vault', 'balance', 'stmt', 'banker', 'teller', 'debit', 'mastercard', 'visa', 'amex', 'paypal', 'venmo', 'stripe', 'zelle', 'exness', 'revolut', 'wise', 'klarna', 'neteller', 'tranglo', 'pionex', 'emiratesnbd', 'yoomoney', 'koronapay', 'wirex', 'paysend', 'alrajhibank', 'transfergo', 'fedbnk', 'hdfcbk', 'stanbic', 'vantage', 'bitget', 'kuveytturk', 'garanti', 'landbank', 'piraeus', 'nedbank', 'monzo', 'n26', 'chime', 'sofi', 'robinhood', 'coinbase', 'kraken', 'kucoin', 'bybit', 'bitmex', 'bitstamp', 'gemini', 'blockchain', 'tether', 'usdt', 'binance', 'matchmove', 'floa', 'zasta', 'tipalti', 'piraeus', 'etoro', 'iqos', 'csair', 'allyspin', 'adac karte', 'nickel', 'taptapsend', 'trusteeplus', 'monetique', 'sumup', 'simple', 'coverflex', 'axa', 'bunq', 'finkredit'],
                    "E-Commerce": ['shop', 'store', 'mall', 'market', 'cart', 'buy', 'deals', 'sale', 'fashion', 'grocery', 'amazon', 'ebay', 'aliexpress', 'shopee', 'lazada', 'flipkart', 'walmart', 'target', 'brand', 'retail', 'pos', 'kiosk', 'coupon', 'voucher', 'order', 'merch', 'boutique', 'clothe', 'shoe', 'marketplace', 'vendor', 'selling', 'buy', 'shop', 'outlet', 'ecommerce', 'checkout', 'parcel', 'logistics', 'delivery', 'daraz', 'hacoo', 'alibaba', 'temu', 'shein', 'farfetch', 'applestore', 'bestbuy', 'costco', 'asos', 'zara', 'hm', 'nike', 'adidas', 'shopback', 'zid', 'farfetch', 'catawiki', 'market', 'pinduoduo', 'vinted', 'lc waikiki', 'olx', 'hepsiburada', 'ozon', 'knuspr', 'iherb', 'jumia', 'jysk'],
                    "Social/Media": ['chat', 'social', 'meet', 'date', 'talk', 'message', 'video', 'stream', 'live', 'fan', 'social', 'post', 'status', 'follow', 'messenger', 'viber', 'telegram', 'whatsapp', 'signal', 'wechat', 'tinder', 'bumble', 'discord', 'reels', 'tiktok', 'snapchat', 'insta', 'tweet', 'blog', 'forum', 'socail', 'network', 'profile', 'story', 'reel', 'vlog', 'community', 'club', 'celebrity', 'influencer', 'emoji', 'sticker', 'gif', 'talk', 'voip', 'badoo', 'kakaotalk', 'imo', 'alipay', 'botim', 'bigo', 'okru', 'bereal', 'line', 'vshow', 'fb inc', 'facebook', 'muzz', 'talkin', 'mbc', 'glow', 'lark', 'yappy', 'tawasal', 'snap', 'soulchill', 'jaco', 'amo', 'naver', 'yalla', 'happn', 'tangome'],
                    "Lifestyle/Travel": ['delivery', 'food', 'eat', 'order', 'taxi', 'ride', 'travel', 'trip', 'hotel', 'flight', 'booking', 'bus', 'train', 'airline', 'resort', 'vacation', 'uber', 'grab', 'bolt', 'foodpanda', 'zomato', 'swiggy', 'doordash', 'deliveroo', 'map', 'tourism', 'guide', 'passport', 'visa', 'rent', 'lease', 'home', 'house', 'room', 'apartment', 'flat', 'stay', 'car', 'auto', 'vehicle', 'parking', 'fuel', 'gas', 'electric', 'weather', 'news', 'airasia', 'careem', 'yandex', 'trip.com', 'gulfair', 'sixt', 'expedia', 'trivago', 'kayak', 'skyscanner', 'agoda', 'booking', 'airbnb', 'hilton', 'marriott', 'delta', 'emirates', 'qatar', 'ryanair', 'indrive', 'yango', 'glovo', 'uberegypt', 'taxsee', 'sixt', 'gulfair', 'turo', 'ajet', 'qunar', 'tuda', 'meituan', 'zenchef', 'dragonpass', 'bikemi'],
                    "Gaming/Entertainment": ['game', 'play', 'fun', 'poker', 'casino', 'bet', 'slot', 'puzzle', 'action', 'rpg', 'mmo', 'strategy', 'arcade', 'simulator', 'quest', 'win', 'prize', 'spin', 'card', 'board', 'adventure', 'craft', 'battle', 'strike', 'combat', 'war', 'hero', 'legend', 'quest', 'gamer', 'gaming', 'esports', 'twitch', 'steam', 'xbox', 'playstation', 'nintendo', 'unity', 'unreal', 'console', 'controller', 'joystick', 'pubgm', 'wargaming', 'razer', 'monopoly', '1xslots', 'slots', 'roblox', 'minecraft', 'fortnite', 'pubg', 'freefire', 'genshin', 'candycrush', 'pokemon', 'clash', 'brawl', 'amongus', 'pubgm', 'razer', 'monopoly go', 'wargaming', 'footballnet', 'ubisoft', 'onemt', 'medal'],
                    "Health/Fitness": ['health', 'doctor', 'clinic', 'workout', 'gym', 'pharmacy', 'fitness', 'medical', 'hospital', 'yoga', 'meditation', 'sleep', 'period', 'cycle', 'track', 'calorie', 'step', 'nurse', 'appointment', 'patient', 'lab', 'medicine', 'drug', 'care', 'well', 'heart', 'body', 'mental', 'therapy', 'dental', 'vision', 'diet', 'nutrition', 'weight', 'muscle', 'training', 'pulse', 'bp', 'sugar', 'glucose', 'doctolib', 'cigna', 'prudential', 'flo', 'fitandgo', 'nuvosana'],
                    "Education/Learning": ['school', 'university', 'learn', 'course', 'quiz', 'student', 'study', 'education', 'academy', 'tutor', 'exam', 'result', 'portal', 'class', 'teacher', 'lesson', 'skill', 'language', 'read', 'write', 'math', 'science', 'history', 'dictionary', 'vocabulary', 'prep', 'homework', 'lecture', 'degree', 'diploma', 'certificate', 'campus', 'admission', 'library', 'textbook', 'e-learning', 'superprof', 'duolingo', 'coursera', 'udemy', 'khan', 'westernu'],
                    "Government/Public": ['gov', 'passport', 'citizen', 'tax', ' id ', 'vote', 'official', 'public', 'service', 'national', 'ministry', 'police', 'emergency', 'utility', 'bill', 'electric', 'water', 'gas', 'council', 'election', 'permit', 'license', 'registry', 'pension', 'benefit', 'social security', 'aadhaar', 'voter', 'pan', 'gst', 'income tax', 'municipal', 'city', 'state', 'federal', 'official', 'hm passport', 'vfs', 'digid', 'tawakkalna'],
                    "Navigation/Maps": ['map', 'gps', 'navigate', 'direction', 'location', 'radar', 'drive', 'traffic', 'compass', 'street', 'route', 'tracking', 'finder', 'way', 'address', 'postal', 'coordinate', 'earth', 'world', 'transit', 'speed', 'speedo', 'trip', 'odometer', 'navigation', 'lane', 'parking', 'fuel', 'ev', 'taxsee', 'waze'],
                    "Music/Audio": ['music', 'radio', 'mp3', 'player', 'song', 'podcast', 'audio', 'sound', 'dj', 'mix', 'equalizer', 'spotify', 'deezer', 'shazam', 'recorder', 'voice', 'sing', 'karaoke', 'instrument', 'guitar', 'piano', 'beat', 'rhythm', 'tune', 'tuner', 'streaming', 'album', 'artist', 'track', 'playlist', 'lyrics', 'tidal', 'soundcloud', 'pandora', 'apple music', 'yt music', 'megogo', 'anghami'],
                    "Photography/Video": ['photo', 'camera', 'editor', 'gallery', 'video', 'clip', 'collage', 'beauty', 'filter', 'lens', 'selfie', 'retouch', 'frame', 'album', 'shot', 'capture', 'movie', 'cinema', 'player', 'vlc', 'netflix', 'youtube', 'prime', 'hulu', 'disney', 'tv', 'show', 'ott', 'vlog', 'reels', 'cinema', 'theatre', 'broadcasting', 'production', 'vlc', 'mx player', 'kmplayer', 'plex', 'kodi', 'megogo', 'max', 'bilibili', 'ivi'],
                    "News/Books": ['news', 'book', 'reader', 'paper', 'magazine', 'novel', 'daily', 'times', 'post', 'journal', 'headline', 'article', 'feed', 'rss', 'library', 'story', 'author', 'kindle', 'pdf', 'epub', 'comic', 'manga', 'shelf', 'publisher', 'medium', 'newspaper', 'bulletin', 'report', 'press', 'literary', 'bbc', 'cnn', 'nytimes', 'wsj', 'reuters', 'guardian'],
                    "Business/Work": ['meeting', 'zoom', 'office', 'work', 'job', 'recruit', 'business', 'resume', 'teams', 'hr', 'staff', 'employee', 'enterprise', 'crm', 'erp', 'slack', 'outlook', 'mail', 'calendar', 'task', 'project', 'collab', 'management', 'admin', 'hiring', 'interview', 'salary', 'payroll', 'expense', 'inc', 'corp', 'company', 'startup', 'client', 'partner', 'github', 'docusign', 'linkedin', 'xing', 'lark', 'calendly', 'tipalti', 'trello', 'asana', 'monday', 'notion', 'clickup', 'basecamp', 'mailchimp', 'microsoft', 'claude', 'indeed', 'vercel', 'realadvisor'],
                    "Betting/Gambling": ['bet', 'win', 'casino', 'slot', 'poker', 'gambling', '1win', 'pin-up', 'betpawa', 'betwinner', '888starz', 'megapari', 'winwin', 'linebet', 'melbet', 'mostbet', 'parimatch', 'betway', 'dafabet', '1xbet', 'pinup', 'paripulse', 'premierbet', 'marathon', 'parimatch', 'betfair', 'williamhill', 'bet365', 'draftkings', 'fanduel', 'sporty', '1xslots', 'betssonarcb', 'premierbet', 'marathon', 'tiger'],
                    "Telecom/OTP": ['sms', 'verify', 'otp', 'auth', 'code', 'link', 'msg', 'notif', 'cloud', 'vonage', 'sinch', 'twilio', 'nexmo', 'plvrfy', 'itcotp', 'smsto', 'duosec', 'msgdog', 'stripelink', 'sinchverify', 'authmsg', 'verify', 'notify', 'bilgimsj', 'message', 'iot sms', 'smsinfo', 'clickotp', 'tcloud', 'bipsms', 'vgsms', 'worldnettps', 'mxt', 'infobip', 'passcode', 'vonagevf', 'tcell wifi', 'clickotp', 'smsinfo', 'iot sms', 'oneapi', 'nxcomm', 'byteplus'],
                    "Logistics/Transport": ['delivery', 'courier', 'parcel', 'ship', 'cargo', 'logistic', 'taxi', 'ride', 'uber', 'grab', 'bolt', 'yango', 'yandex', 'toters', 'careem', 'indrive', 'lalamove', 'foodpanda', 'doordash', 'deliveroo', 'glovo', 'rappi', 'talabat', 'deliveryhero', 'uberegypt', 'taxsee', 'sixt', 'sixt', 'hertz', 'avis', 'budget', 'enterprise', 'dhl'],
                    "Tools/Security": ['vpn', 'proxy', 'secure', 'protect', 'antivirus', 'cleaner', 'battery', 'tool', 'file', 'manager', 'browser', 'web', 'launcher', 'theme', 'font', 'keyboard', 'calculator', 'clock', 'alarm', 'weather', 'widget', 'backup', 'restore', 'scan', 'zip', 'rar', 'authenticator', 'otp', 'checker', 'speedtest', 'mirror', 'converter', 'explorer', 'root', 'super', 'flash', 'light', 'torch', 'wifi', 'signal', 'network', 'camscanner', 'am secure', 't-mob', 'samsung', 'xiaomi', 'huawei', 'apple', 'google', 'realme', 'honor', 'oppo', 'vivo', 'asus', 'sony', 'lg', 'ezviz', 'duosec', 'galaxy', 'jia']
                }

                for category, keywords in cat_map.items():
                    if any(k in n for k in keywords):
                        return category
                
                # Numeric IDs are usually OTP shortcodes
                if tid.isdigit():
                    return "Telecom/OTP"
                    
                return "UNCATEGORIZED"

            cat = guess_category(name, tid, row.get("Description", ""), row.get("Sample_Message", ""))
            
            # Improved Tier/Difficulty Logic
            raw_tier = row.get("Tier", "").strip()
            if not raw_tier:
                # Guess difficulty based on category if Tier is missing
                easy_cats = ["Telecom/OTP", "Social/Media", "Tools/Security", "Lifestyle/Travel"]
                med_cats = ["Gaming/Entertainment", "E-Commerce", "Business/Work", "Navigation/Maps"]
                
                if cat in easy_cats:
                    tier = "Tier 1 (Instant/Public)"
                elif cat in med_cats:
                    tier = "Tier 2 (Moderate/Private)"
                else:
                    tier = "Tier 3 (Hard/Secured)"
            else:
                tier = raw_tier

            if tid in SECURITY_INTEL:
                diff = SECURITY_INTEL[tid]
                reason = f"Score {diff}: {cat} (Verified intelligence)."
            else:
                reason = TIER_MAP.get(tier, f"Base score {base_score}: {cat}.")
                # Assign scores
                if "Tier 1" in tier: diff = 50
                elif "Tier 2" in tier: diff = 50
                else: diff = 50
            
            triggers = []
            is_nf = nf_dict.get(tid, False) or "not found" in row.get("Description", "").lower()
            if is_nf: 
                diff, triggers = 100, ["Binary Not Found"]
            
            final_data.append({
                "id": tid,
                "name": name,
                "sms": row.get("Sample_Message", ""),
                "claimed": claimed,
                "root_detected": root_dict.get(tid, False),
                "not_found": is_nf,
                "note": note,
                "is_new": tid not in claims_dict and tid not in notes_dict and tid not in root_dict and tid not in nf_dict and tid not in updated_dict,
                "difficulty": diff,
                "category": cat,
                "tier": tier,
                "reason": reason,
                "triggers": triggers,
                "last_updated": row.get("Last_Updated", "2024-05-09"),
                "urls": {
                    "play": f"https://play.google.com/store/apps/details?id={tid}",
                    "pure": f"https://apkpure.com/search?q={tid}",
                    "mirror": f"https://www.apkmirror.com/?post_type=app_release&searchtype=apk&s={tid}",
                    "uptodown": f"https://en.uptodown.com/android/search/{tid}",
                    "aptoide": f"https://{tid}.en.aptoide.com/app"
                }
            })

    # Preserve original CSV order (do NOT sort - order comes from fresh_detailed.csv)
    
    with open(OUTPUT_JS, "w", encoding="utf-8") as f:
        f.write(f"window.apkhunterData = {json.dumps(final_data, indent=4)};")
    
    print(f"[*] Processed {len(final_data)} targets.")
    print(f"[+] Sync Complete: {OUTPUT_JS}")

if __name__ == "__main__":
    sync()
