import os
import json
import csv
import urllib.parse
from datetime import datetime

# --- CONFIGURATION ---
PORTAL_DIR = r"C:\HTB-Notes-Portal"
CSV_FILE = os.path.join(PORTAL_DIR, "fresh_detailed.csv")
DB_FILE = os.path.join(PORTAL_DIR, "apk_local_database.json")
OUTPUT_FILE = os.path.join(os.getcwd(), "dashboard", "apkhunter_data.js")

# --- SECURITY INTELLIGENCE (Mirrored from ApkHunter.py) ---
SECURITY_INTEL = {
    "signal": 98, "whatsapp": 95, "yoomoney": 95, "ing": 95, "payoneer": 95, 
    "openbank": 95, "wise": 95, "revolut": 95, "boursorama": 95, "plus500": 95,
    "binance": 95, "okx": 95, "ziraatbank": 95, "citibank": 95, "pnc": 95,
    "bolt": 90, "uber": 90, "dhl": 90, "fedex": 85, "airasia": 88, "yandex": 90, 
    "tsb": 95, "gaijin": 90, "steam": 85, "tfl": 85, "grab": 90, "lalamove": 85,
    "fpmarkets": 85, "doctolib": 85, "lidl": 85, "etoro": 88,
    "aliexpress": 85, "shopee": 80, "adidas": 75, "nike": 75, "temu": 75, "shein": 75,
    "airbnb": 75, "leboncoin": 75, "marktplaats": 75, "wallapop": 75,
    "fiverr": 75, "up": 75, "vinted": 75, "shopeepay": 80,
    "tinder": 65, "bumble": 65, "okcupid": 65, "bigo": 70, "garmin": 65, "fiverr": 45, 
    "vonage": 45, "quora": 40, "tunecore": 30, "indeed": 35, "mixpanel": 25,
    "gofundme": 50, "cigna": 60, "prudential": 60, "cgd": 60, "bankera": 60, "lego": 50
}

def load_db():
    if not os.path.exists(DB_FILE): 
        return {"claimed":{},"notes":{},"issues":{},"root_detected":{},"not_found":{},"last_updated":{}}
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except: 
            return {"claimed":{},"notes":{},"issues":{},"root_detected":{},"not_found":{},"last_updated":{}}

def sync():
    print(f"[*] Starting APKHunter Sync...")
    db = load_db()
    c_d = db.get("claimed", {})
    n_d = db.get("notes", {})
    i_d = db.get("issues", {})
    r_d = db.get("root_detected", {})
    nf_d = db.get("not_found", {})
    u_d = db.get("last_updated", {})
    
    targets = []
    
    if not os.path.exists(CSV_FILE):
        print(f"[!] Error: {CSV_FILE} not found.")
        return

    TIER_MAP = {
        "Tier 2: SMS OTP Only": "Standard Tier 2 service (SMS-only flow).",
        "Tier 1: No 2FA / Unknown": "Legacy Tier 1 service. Minimal security.",
        "Tier 2: OTP Only": "Standard Tier 2 service (OTP-only flow).",
        "Tier 1: High Security": "Tier 1 High-Security service."
    }

    with open(CSV_FILE, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("Name") or "Unknown").strip()
            tid = (row.get("API_ID") or row.get("Slug") or "").strip().lower()
            tier = (row.get("Category") or "Unknown").strip()
            
            if not tid: tid = "missing_id_" + str(hash(name))
            
            is_c = c_d.get(tid, False)
            is_r = r_d.get(tid, False)
            is_nf = nf_d.get(tid, False)
            note = n_d.get(tid, "").strip()
            
            base_score = SECURITY_INTEL.get(tid, 45) # Default to 45 (Moderate-Easy)
            diff = base_score
            
            p_issues = i_d.get(tid, [])
            intel_pool = (" ".join([str(x.get('text','')).lower() for x in p_issues]) + " " + note.lower()).strip()
            
            # --- ELITE CATEGORIZATION ENGINE ---
            def guess_category(name, tid, desc="", sms=""):
                n = (name.lower() + " " + tid.lower() + " " + desc.lower() + " " + (sms or "").lower()).replace('.', ' ')
                
                cat_map = {
                    "Banking/Fintech": ['bank', 'pay', 'wallet', 'finance', 'invest', 'crypto', 'coin', 'trading', 'broker', 'card', 'loan', 'credit', 'money', 'cash', 'transfer', 'ledger', 'stock', 'forex', 'capital', 'wealth', 'save', 'budget', 'billing', 'invoice', 'checkout', 'pos', 'payment', 'atm', 'remit', 'paisa', 'khata', 'upi', 'fintech', 'merchant', 'mortgage', 'insurance', 'repay', 'interest', 'vault', 'balance', 'stmt', 'banker', 'teller', 'debit', 'mastercard', 'visa', 'amex', 'paypal', 'venmo', 'stripe', 'zelle', 'exness', 'revolut', 'wise', 'klarna', 'neteller', 'tranglo', 'pionex', 'emiratesnbd', 'yoomoney', 'koronapay', 'wirex', 'paysend', 'alrajhibank', 'transfergo', 'fedbnk', 'hdfcbk', 'stanbic', 'vantage', 'bitget', 'kuveytturk', 'garanti', 'landbank', 'piraeus', 'nedbank', 'monzo', 'n26', 'chime', 'sofi', 'robinhood', 'coinbase', 'kraken', 'kucoin', 'bybit', 'bitmex', 'bitstamp', 'gemini', 'blockchain', 'tether', 'usdt', 'binance'],
                    "E-Commerce": ['shop', 'store', 'mall', 'market', 'cart', 'buy', 'deals', 'sale', 'fashion', 'grocery', 'amazon', 'ebay', 'aliexpress', 'shopee', 'lazada', 'flipkart', 'walmart', 'target', 'brand', 'retail', 'pos', 'kiosk', 'coupon', 'voucher', 'order', 'merch', 'boutique', 'clothe', 'shoe', 'marketplace', 'vendor', 'selling', 'buy', 'shop', 'outlet', 'ecommerce', 'checkout', 'parcel', 'logistics', 'delivery', 'daraz', 'hacoo', 'alibaba', 'temu', 'shein', 'farfetch', 'applestore', 'bestbuy', 'costco', 'asos', 'zara', 'hm', 'nike', 'adidas'],
                    "Social/Media": ['chat', 'social', 'meet', 'date', 'talk', 'message', 'video', 'stream', 'live', 'fan', 'social', 'post', 'status', 'follow', 'messenger', 'viber', 'telegram', 'whatsapp', 'signal', 'wechat', 'tinder', 'bumble', 'discord', 'reels', 'tiktok', 'snapchat', 'insta', 'tweet', 'blog', 'forum', 'socail', 'network', 'profile', 'story', 'reel', 'vlog', 'community', 'club', 'celebrity', 'influencer', 'emoji', 'sticker', 'gif', 'talk', 'voip', 'badoo', 'kakaotalk', 'imo', 'alipay', 'botim', 'bigo', 'okru', 'bereal', 'line', 'vshow', 'fb inc', 'facebook'],
                    "Lifestyle/Travel": ['delivery', 'food', 'eat', 'order', 'taxi', 'ride', 'travel', 'trip', 'hotel', 'flight', 'booking', 'bus', 'train', 'airline', 'resort', 'vacation', 'uber', 'grab', 'bolt', 'foodpanda', 'zomato', 'swiggy', 'doordash', 'deliveroo', 'map', 'tourism', 'guide', 'passport', 'visa', 'rent', 'lease', 'home', 'house', 'room', 'apartment', 'flat', 'stay', 'car', 'auto', 'vehicle', 'parking', 'fuel', 'gas', 'electric', 'weather', 'news', 'airasia', 'careem', 'yandex', 'trip.com', 'gulfair', 'sixt', 'expedia', 'trivago', 'kayak', 'skyscanner', 'agoda', 'booking', 'airbnb', 'hilton', 'marriott', 'delta', 'emirates', 'qatar', 'ryanair', 'indrive', 'yango'],
                    "Gaming/Entertainment": ['game', 'play', 'fun', 'poker', 'casino', 'bet', 'slot', 'puzzle', 'action', 'rpg', 'mmo', 'strategy', 'arcade', 'simulator', 'quest', 'win', 'prize', 'spin', 'card', 'board', 'adventure', 'craft', 'battle', 'strike', 'combat', 'war', 'hero', 'legend', 'quest', 'gamer', 'gaming', 'esports', 'twitch', 'steam', 'xbox', 'playstation', 'nintendo', 'unity', 'unreal', 'console', 'controller', 'joystick', 'pubgm', 'wargaming', 'razer', 'monopoly', '1xslots', 'slots', 'roblox', 'minecraft', 'fortnite', 'pubg', 'freefire', 'genshin', 'candycrush', 'pokemon', 'clash', 'brawl', 'amongus'],
                    "Health/Fitness": ['health', 'doctor', 'clinic', 'workout', 'gym', 'pharmacy', 'fitness', 'medical', 'hospital', 'yoga', 'meditation', 'sleep', 'period', 'cycle', 'track', 'calorie', 'step', 'nurse', 'appointment', 'patient', 'lab', 'medicine', 'drug', 'care', 'well', 'heart', 'body', 'mental', 'therapy', 'dental', 'vision', 'diet', 'nutrition', 'weight', 'muscle', 'training', 'pulse', 'bp', 'sugar', 'glucose', 'doctolib', 'cigna', 'prudential'],
                    "Education/Learning": ['school', 'university', 'learn', 'course', 'quiz', 'student', 'study', 'education', 'academy', 'tutor', 'exam', 'result', 'portal', 'class', 'teacher', 'lesson', 'skill', 'language', 'read', 'write', 'math', 'science', 'history', 'dictionary', 'vocabulary', 'prep', 'homework', 'lecture', 'degree', 'diploma', 'certificate', 'campus', 'admission', 'library', 'textbook', 'e-learning', 'superprof', 'duolingo', 'coursera', 'udemy', 'khan'],
                    "Government/Public": ['gov', 'passport', 'citizen', 'tax', ' id ', 'vote', 'official', 'public', 'service', 'national', 'ministry', 'police', 'emergency', 'utility', 'bill', 'electric', 'water', 'gas', 'council', 'election', 'permit', 'license', 'registry', 'pension', 'benefit', 'social security', 'aadhaar', 'voter', 'pan', 'gst', 'income tax', 'municipal', 'city', 'state', 'federal', 'official', 'hm passport', 'vfs', 'digid'],
                    "Navigation/Maps": ['map', 'gps', 'navigate', 'direction', 'location', 'radar', 'drive', 'traffic', 'compass', 'street', 'route', 'tracking', 'finder', 'way', 'address', 'postal', 'coordinate', 'earth', 'world', 'transit', 'speed', 'speedo', 'trip', 'odometer', 'navigation', 'lane', 'parking', 'fuel', 'ev', 'taxsee', 'waze'],
                    "Music/Audio": ['music', 'radio', 'mp3', 'player', 'song', 'podcast', 'audio', 'sound', 'dj', 'mix', 'equalizer', 'spotify', 'deezer', 'shazam', 'recorder', 'voice', 'sing', 'karaoke', 'instrument', 'guitar', 'piano', 'beat', 'rhythm', 'tune', 'tuner', 'streaming', 'album', 'artist', 'track', 'playlist', 'lyrics', 'tidal', 'soundcloud', 'pandora', 'apple music', 'yt music'],
                    "Photography/Video": ['photo', 'camera', 'editor', 'gallery', 'video', 'clip', 'collage', 'beauty', 'filter', 'lens', 'selfie', 'retouch', 'frame', 'album', 'shot', 'capture', 'movie', 'cinema', 'player', 'vlc', 'netflix', 'youtube', 'prime', 'hulu', 'disney', 'tv', 'show', 'ott', 'vlog', 'reels', 'cinema', 'theatre', 'broadcasting', 'production', 'vlc', 'mx player', 'kmplayer', 'plex', 'kodi', 'megogo'],
                    "News/Books": ['news', 'book', 'reader', 'paper', 'magazine', 'novel', 'daily', 'times', 'post', 'journal', 'headline', 'article', 'feed', 'rss', 'library', 'story', 'author', 'kindle', 'pdf', 'epub', 'comic', 'manga', 'shelf', 'publisher', 'medium', 'newspaper', 'bulletin', 'report', 'press', 'literary', 'bbc', 'cnn', 'nytimes', 'wsj', 'reuters', 'guardian'],
                    "Business/Work": ['meeting', 'zoom', 'office', 'work', 'job', 'recruit', 'business', 'resume', 'teams', 'hr', 'staff', 'employee', 'enterprise', 'crm', 'erp', 'slack', 'outlook', 'mail', 'calendar', 'task', 'project', 'collab', 'management', 'admin', 'hiring', 'interview', 'salary', 'payroll', 'expense', 'inc', 'corp', 'company', 'startup', 'client', 'partner', 'github', 'docusign', 'linkedin', 'xing', 'lark', 'calendly', 'tipalti', 'trello', 'asana', 'monday', 'notion', 'clickup', 'basecamp'],
                    "Betting/Gambling": ['bet', 'win', 'casino', 'slot', 'poker', 'gambling', '1win', 'pin-up', 'betpawa', 'betwinner', '888starz', 'megapari', 'winwin', 'linebet', 'melbet', 'mostbet', 'parimatch', 'betway', 'dafabet', '1xbet', 'pinup', 'paripulse', 'premierbet', 'marathon', 'parimatch', 'betfair', 'williamhill', 'bet365', 'draftkings', 'fanduel'],
                    "Telecom/OTP": ['sms', 'verify', 'otp', 'auth', 'code', 'link', 'msg', 'notif', 'cloud', 'vonage', 'sinch', 'twilio', 'nexmo', 'plvrfy', 'itcotp', 'smsto', 'duosec', 'msgdog', 'stripelink', 'sinchverify', 'authmsg', 'verify', 'notify', 'bilgimsj', 'message', 'iot sms', 'smsinfo', 'clickotp', 'tcloud', 'bipsms', 'vgsms', 'worldnettps', 'mxt', 'infobip', 'passcode'],
                    "Logistics/Transport": ['delivery', 'courier', 'parcel', 'ship', 'cargo', 'logistic', 'taxi', 'ride', 'uber', 'grab', 'bolt', 'yango', 'yandex', 'toters', 'careem', 'indrive', 'lalamove', 'foodpanda', 'doordash', 'deliveroo', 'glovo', 'rappi', 'talabat', 'deliveryhero', 'uberegypt', 'taxsee', 'sixt', 'sixt', 'hertz', 'avis', 'budget', 'enterprise'],
                    "Tools/Security": ['vpn', 'proxy', 'secure', 'protect', 'antivirus', 'cleaner', 'battery', 'tool', 'file', 'manager', 'browser', 'web', 'launcher', 'theme', 'font', 'keyboard', 'calculator', 'clock', 'alarm', 'weather', 'widget', 'backup', 'restore', 'scan', 'zip', 'rar', 'authenticator', 'otp', 'checker', 'speedtest', 'mirror', 'converter', 'explorer', 'root', 'super', 'flash', 'light', 'torch', 'wifi', 'signal', 'network', 'camscanner', 'am secure', 't-mob', 'samsung', 'xiaomi', 'huawei', 'apple', 'google', 'realme', 'honor', 'oppo', 'vivo', 'asus', 'sony', 'lg']
                }

                for category, keywords in cat_map.items():
                    if any(k in n for k in keywords):
                        return category
                
                # Numeric IDs are usually OTP shortcodes
                if tid.isdigit():
                    return "Telecom/OTP"
                    
                return "UNCATEGORIZED"

            cat = guess_category(name, tid, row.get("Description", ""), row.get("Sample_Message", ""))
            
            if tid in SECURITY_INTEL:
                diff = SECURITY_INTEL[tid]
                reason = f"Score {diff}: {cat} (Verified intelligence)."
            else:
                reason = TIER_MAP.get(tier, f"Base score {base_score}: {cat}.")
            
            # Adjust score based on tier if unknown
            if tid not in SECURITY_INTEL:
                if "Tier 1" in tier: diff = 35 # Explicitly Easy
                elif "Tier 2" in tier: diff = 65 # Moderate
            
            triggers = []
            if is_nf: 
                diff, triggers = 100, ["Binary Not Found"]
            
            flow_keywords = ["no web flow", "no phone", "no endpoint", "only available on mobile"]
            found_flow = [k for k in flow_keywords if k in intel_pool]
            if found_flow:
                diff = max(diff, 95)
                triggers.append(f"No Endpoint ({found_flow[0]})")

            ssl_keywords = ["pinning", "ssl", "flutter"]
            found_ssl = [k for k in ssl_keywords if k in intel_pool]
            if found_ssl:
                diff = max(diff, 90)
                triggers.append(f"Hard Security ({found_ssl[0]})")

            trigger_explanations = {
                "Binary Not Found": "Scrapers failed to locate the APK binary across known mirrors. Manual acquisition required.",
                "No Endpoint": "Potential lack of standard web/phone endpoints; research suggests mobile-only or hidden flows.",
                "Hard Security": "Protections like SSL Pinning or Flutter detected in intelligence logs. Significant research effort expected."
            }
            
            if triggers:
                expls = [trigger_explanations.get(t.split(' (')[0], t) for t in triggers]
                reason = f"Critical Hurdles: {' '.join(expls)}"
            elif tid in SECURITY_INTEL:
                reason = f"Target verified as {cat}. Known security posture: {diff}/100."
            else:
                reason = f"Standard {cat} service. No specific security hurdles identified in intelligence logs."
            
            final_diff = int(max(0, min(100, diff)))
            
            q = urllib.parse.quote_plus(name)
            targets.append({
                "id": tid, "name": name, "sms": row.get("Sample_Message", ""), 
                "claimed": is_c, "note": note, "root_detected": is_r, "not_found": is_nf,
                "difficulty": final_diff, "reason": reason, "category": cat,
                "last_updated": u_d.get(tid, "NEVER"),
                "urls": {
                    "play": f"https://play.google.com/store/search?q={q}&c=apps",
                    "pure": f"https://apkpure.net/search?q={q}",
                    "aptoide": f"https://en.aptoide.com/search?query={q}",
                    "mirror": f"https://www.apkmirror.com/?searchtype=apk&s={q}",
                    "uptodown": f"https://en.uptodown.com/android/search?q={q}"
                }
            })

    print(f"[*] Processed {len(targets)} targets.")
    
    # Sort by difficulty descending for high-value targets first
    targets.sort(key=lambda x: x['difficulty'], reverse=True)

    # Load token for injection
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if line.startswith("GITHUB_TOKEN="):
                        token = line.split("=", 1)[1].strip()

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"window.GH_TOKEN_INJECTED = '';\n")
        f.write(f"window.apkhunterData = {json.dumps(targets, indent=2)};\n")
        f.write(f"window.apkhunterLastSync = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}';\n")
    
    print(f"[+] Sync Complete: {OUTPUT_FILE}")

if __name__ == "__main__":
    sync()
