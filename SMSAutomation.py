import requests
import time
import json
import os

# --- Configuration ---
IP = "62.238.2.204"
ACCESS_PORT = "3666"        # Port for the dynamic provider list
API_PORT = "8090"           # Port for the core SMS API
TOKEN = "Scxfqcsgg"
DB_FILE = "operator_database_clean.json" # Your local offline database

# --- Dial Code Mapping ---
COUNTRY_DIAL_CODES = {
    "AD": "+376", "AE": "+971", "AF": "+93", "AG": "+1", "AI": "+1", "AL": "+355", "AM": "+374", "AO": "+244", "AR": "+54", "AS": "+1",
    "AT": "+43", "AU": "+61", "AW": "+297", "AZ": "+994", "BA": "+387", "BB": "+1", "BD": "+880", "BE": "+32", "BF": "+226", "BG": "+359",
    "BH": "+973", "BI": "+257", "BJ": "+229", "BM": "+1", "BN": "+673", "BO": "+591", "BR": "+55", "BS": "+1", "BT": "+975", "BW": "+267",
    "BY": "+375", "BZ": "+501", "CA": "+1", "CD": "+243", "CF": "+236", "CG": "+242", "CH": "+41", "CI": "+225", "CK": "+682", "CL": "+56",
    "CM": "+237", "CN": "+86", "CO": "+57", "CR": "+506", "CU": "+53", "CV": "+238", "CW": "+599", "CY": "+357", "CZ": "+420", "DE": "+49",
    "DJ": "+253", "DK": "+45", "DM": "+1", "DO": "+1", "DZ": "+213", "EC": "+593", "EE": "+372", "EG": "+20", "ER": "+291", "ES": "+34",
    "ET": "+251", "FI": "+358", "FJ": "+679", "FK": "+500", "FM": "+691", "FO": "+298", "FR": "+33", "GA": "+241", "GB": "+44", "GD": "+1",
    "GE": "+995", "GF": "+594", "GH": "+233", "GI": "+350", "GL": "+299", "GM": "+220", "GN": "+224", "GP": "+590", "GQ": "+240", "GR": "+30",
    "GT": "+502", "GU": "+1", "GW": "+245", "GY": "+592", "HK": "+852", "HN": "+504", "HR": "+385", "HT": "+509", "HU": "+36", "ID": "+62",
    "IE": "+353", "IL": "+972", "IM": "+44", "IN": "+91", "IO": "+246", "IQ": "+964", "IR": "+98", "IS": "+354", "IT": "+39", "JE": "+44",
    "JM": "+1", "JO": "+962", "JP": "+81", "KE": "+254", "KG": "+996", "KH": "+855", "KI": "+686", "KM": "+269", "KN": "+1", "KP": "+850",
    "KR": "+82", "KW": "+965", "KY": "+1", "KZ": "+7", "LA": "+856", "LB": "+961", "LC": "+1", "LI": "+423", "LK": "+94", "LR": "+231",
    "LS": "+266", "LT": "+370", "LU": "+352", "LV": "+371", "LY": "+218", "MA": "+212", "MC": "+377", "MD": "+373", "ME": "+382", "MF": "+590",
    "MG": "+261", "MH": "+692", "MK": "+389", "ML": "+223", "MM": "+95", "MN": "+976", "MO": "+853", "MP": "+1", "MQ": "+596", "MR": "+222",
    "MS": "+1", "MT": "+356", "MU": "+230", "MV": "+960", "MW": "+265", "MX": "+52", "MY": "+60", "MZ": "+258", "NA": "+264", "NC": "+687",
    "NE": "+227", "NF": "+672", "NG": "+234", "NI": "+505", "NL": "+31", "NO": "+47", "NP": "+977", "NR": "+674", "NU": "+683", "NZ": "+64",
    "OM": "+968", "PA": "+507", "PE": "+51", "PF": "+689", "PG": "+675", "PH": "+63", "PK": "+92", "PL": "+48", "PM": "+508", "PR": "+1",
    "PS": "+970", "PT": "+351", "PW": "+680", "PY": "+595", "QA": "+974", "RE": "+262", "RO": "+40", "RS": "+381", "RU": "+7", "RW": "+250",
    "SA": "+966", "SB": "+677", "SC": "+248", "SD": "+249", "SE": "+46", "SG": "+65", "SH": "+290", "SI": "+386", "SK": "+421", "SL": "+232",
    "SM": "+378", "SN": "+221", "SO": "+252", "SR": "+597", "SS": "+211", "ST": "+239", "SV": "+503", "SX": "+1", "SY": "+963", "SZ": "+268",
    "TC": "+1", "TD": "+235", "TG": "+228", "TH": "+66", "TJ": "+992", "TK": "+690", "TL": "+670", "TM": "+993", "TN": "+216", "TO": "+676",
    "TR": "+90", "TT": "+1", "TV": "+688", "TW": "+886", "TZ": "+255", "UA": "+380", "UG": "+256", "US": "+1", "UY": "+598", "UZ": "+998",
    "VA": "+379", "VC": "+1", "VE": "+58", "VG": "+1", "VI": "+1", "VN": "+84", "VU": "+678", "WF": "+681", "WS": "+685", "XK": "+383",
    "YE": "+967", "YT": "+262", "ZA": "+27", "ZM": "+260", "ZW": "+263"
}

# --- High Success Operators ---
HIGH_SUCCESS_OPERATORS = {
    "IT": ["fastweb", "windtre", "special", "iliad", "spusu", "tim"]
}

# Splitting the Base URLs to handle the different ports
ACCESS_INFO_URL = f"http://{IP}:{ACCESS_PORT}/accessinfo"
BASE_URL = f"http://{IP}:{API_PORT}/api"

def fetch_dynamic_providers(service_name):
    """Fetches available countries and operators from the Live API."""
    params = {
        "interval": "10min",
        "service": service_name,
        "token": TOKEN
    }
    
    print(f"\n[*] Querying live database on port {ACCESS_PORT} for service: '{service_name}'...")
    try:
        response = requests.get(ACCESS_INFO_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "Data retrieved successfully" and data.get("data"):
            providers = {}
            print(f"\n--- Available Providers for {service_name.upper()} ---")
            print(f"Total Operators: {data.get('total_operators_count')} | Total Access Count: {data.get('total_access_count')}")
            
            for i, item in enumerate(data["data"], start=1):
                ccode = item["ccode"].upper()
                op = item["operator"].lower()
                
                providers[str(i)] = {
                    "country_code": item["ccode"],
                    "operator": item["operator"]
                }
                
                # Highlight high success operators
                highlight = ""
                if ccode in HIGH_SUCCESS_OPERATORS and op in HIGH_SUCCESS_OPERATORS[ccode]:
                    highlight = " [⭐ HIGH SUCCESS RATE]"
                    
                print(f"[{i}] Country: {ccode} ({item['country']}) | Operator: {item['operator'].title()} | Available: {item['access_count']}{highlight}")
            
            return providers
        else:
            print("[-] No active operators found for this service right now.")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"[-] HTTP Error fetching providers: {e}")
        return None

def select_provider(providers):
    """Prompts the user to select an operator from the dynamically generated list."""
    while True:
        choice = input("\n[?] Select a provider ID (or 'b' to go back): ").strip().lower()
        if choice == 'b':
            return None, None
        if choice in providers:
            selected = providers[choice]
            return selected["country_code"], selected["operator"]
        print("[-] Invalid selection. Please choose a valid ID from the list.")

def get_number(country, operator):
    """Fetches a new phone number from the API."""
    url = f"{BASE_URL}/get_numbers"
    
    safe_operator = operator.replace("ü", "u").replace("ö", "o")
    
    params = {
        "country": country,
        "operator": safe_operator, 
        "count": 1,
        "token": TOKEN
    }
    
    print(f"\n[*] Requesting a new {operator.upper()} number in {country} on port {API_PORT}...")
    try:
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"[-] API Error {response.status_code} for URL: {response.url}")
            try:
                print(f"[-] Server Response: {response.json()}")
            except ValueError:
                print(f"[-] Server Response: {response.text}")
            return None

        data = response.json()
        
        if data.get("success") and data.get("number"):
            raw_num = data["number"][0]
            carrier = data.get("carrier", "Unknown")
            
            # Format the dial code
            dial_code = COUNTRY_DIAL_CODES.get(country.upper(), "")
            clean_dial = dial_code.replace("+", "")
            
            display_num = raw_num
            if clean_dial and raw_num.startswith(clean_dial):
                local_part = raw_num[len(clean_dial):]
                display_num = f"{dial_code} {local_part}"
            else:
                display_num = f"+{raw_num}"
                
            print(f"[+] Success! Number obtained: {display_num} ({carrier})")
            return raw_num
        else:
            print(f"[-] Failed to get number. API Response: {data}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"[-] HTTP Error getting number: {e}")
        return None

def wait_for_sms(number, max_retries=15, delay=4):
    """Polls the API for new messages sent to the given number."""
    url = f"{BASE_URL}/get_messages"
    params = {
        "token": TOKEN,
        "number": number
    }
    
    print(f"[*] Waiting for SMS on {number}... (Timeout in {max_retries * delay}s)")
    
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, params=params)
            
            if response.status_code == 400:
                try:
                    data = response.json()
                    if data.get("detail") == "No messages found for the provided number":
                        print(f"[*] Attempt {attempt}/{max_retries}: No messages yet. Retrying in {delay} seconds...")
                        time.sleep(delay)
                        continue
                except ValueError:
                    pass 
            
            response.raise_for_status()
            
            data = response.json()
            print(f"\n[+] Message received!\n{data}")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"[-] HTTP Error checking messages: {e}")
            if 'response' in locals() and response is not None:
                print(f"[-] Server Response: {response.text}")
            time.sleep(delay)
            
    print("\n[-] Timed out waiting for SMS.")
    return None

# ==========================================
# FLOW CONTROLLERS
# ==========================================

def execute_polling_loop(target_country, target_operator):
    """Handles the repetitive loop of getting a number and waiting for SMS."""
    while True:
        phone_number = get_number(target_country, target_operator)
        
        if not phone_number:
            retry = input("[-] Press ENTER to try again, 'p' to pick a new provider, or 'b' to go back: ").strip().lower()
            if retry == 'b':
                return "back_to_menu"
            elif retry == 'p':
                return "pick_new_provider"
            continue
            
        # ---> GENERATING THE CLICKABLE LINK HERE <---
        manual_link = f"{BASE_URL}/get_messages?token={TOKEN}&number={phone_number}"
        
        print(f"\n[!] ACTION REQUIRED: Enter {phone_number} into the target application.")
        print(f"[🔗] Manual SMS Check Link: {manual_link}") # Allows Ctrl+Click in terminal
        
        action = input("[?] Press ENTER to start polling, 'n' to discard & get a NEW number, or 'b' to go back: ").strip().lower()
        
        if action == 'b':
            return "back_to_menu"
        elif action == 'n':
            print("[*] Discarding current number...")
            continue
            
        sms_data = wait_for_sms(phone_number)
        
        next_step = input("\n[?] Test complete. Press ENTER to select a new provider, or 'b' to go back: ").strip().lower()
        if next_step == 'b':
            return "back_to_menu"
        else:
            return "pick_new_provider"

def service_live_flow():
    """Handles the flow when searching by Service using the Live API."""
    while True:
        service_input = input("\n[?] Enter the target service name (e.g., 'tawasal') or 'b' to go back: ").strip().lower()
        if service_input == 'b':
            return
        if not service_input:
            continue
            
        dynamic_providers = fetch_dynamic_providers(service_input)
        if not dynamic_providers:
            continue
            
        while True:
            target_country, target_operator = select_provider(dynamic_providers)
            if not target_country or not target_operator:
                break  
                
            status = execute_polling_loop(target_country, target_operator)
            if status == "back_to_menu":
                return

def service_offline_flow():
    """Handles searching for a specific service exclusively using the Offline Database."""
    if not os.path.exists(DB_FILE):
        print(f"[-] Error: '{DB_FILE}' not found. Please add a service first.")
        return

    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            db = json.load(f)
        except json.JSONDecodeError:
            print(f"[-] Error: {DB_FILE} is corrupted.")
            return

    while True:
        service_input = input("\n[?] Enter Offline Service Name (e.g., 'uber') or 'b' to go back: ").strip().lower()
        if service_input == 'b':
            return
        if not service_input:
            continue

        if service_input not in db:
            print(f"[-] '{service_input}' not found in the offline database. Use the Main Menu to add it first!")
            continue

        raw_providers = db[service_input]
        temp_providers = {}
        
        print(f"\n--- Available Providers for {service_input.upper()} (Offline Data) ---")
        for i, item in enumerate(raw_providers, start=1):
            temp_providers[str(i)] = {
                "country_code": item["ccode"],
                "operator": item["operator"]
            }
            acc_count = item.get('access_count', 'Unknown')
            print(f"[{i}] Country: {item['ccode'].upper()} ({item['country']}) | Operator: {item['operator'].title()} | Cached: {acc_count}")
            
        while True:
            target_country, target_operator = select_provider(temp_providers)
            if not target_country or not target_operator:
                break
                
            status = execute_polling_loop(target_country, target_operator)
            if status == "back_to_menu":
                return

def load_local_database_for_countries():
    """Loads the massive new master JSON database for country searching."""
    master_db_path = r"C:\HTB-Notes-Portal\full_live_operators_db.json"
    if not os.path.exists(master_db_path):
        print(f"[-] Error: Master Database '{master_db_path}' not found. Did you run the builder script?")
        return None
        
    with open(master_db_path, "r", encoding="utf-8") as file:
        try:
            raw_data = json.load(file)
        except json.JSONDecodeError:
            return None
            
    country_db = {}
    for ccode, data in raw_data.items():
        country_db[ccode.upper()] = {
            'name': data.get('country_name', ''),
            'operators': data.get('operators', [])
        }
        
    return country_db

def country_offline_flow():
    """Handles searching offline by Country Code, Name, or Dial Code."""
    country_db = load_local_database_for_countries()
    if not country_db:
        print("[-] Database is empty or corrupted.")
        return
        
    while True:
        search_query = input("\n[?] Enter Name, Code, or Dial Code (e.g., 'Turkey', 'TR', or '+90') or 'b' to go back: ").strip().lower()
        if search_query == 'b':
            return
        if not search_query:
            continue
            
        dial_query = search_query
        if dial_query.isdigit():
            dial_query = "+" + dial_query
            
        matched_ccodes = []
        
        for ccode, details in country_db.items():
            mapped_dial_code = COUNTRY_DIAL_CODES.get(ccode, "").lower()
            
            if (search_query.upper() == ccode or 
                search_query == details['name'].lower() or 
                dial_query == mapped_dial_code):
                matched_ccodes.append(ccode)
                
        if not matched_ccodes:
            print(f"[-] No match found in the database for '{search_query}'.")
            continue
            
        matched_ccode = matched_ccodes[0]
        country_data = country_db[matched_ccode]
        
        temp_providers = {}
        print(f"\n--- Available Operators for {country_data['name'].upper()} ({matched_ccode}) ---")
        for i, operator in enumerate(country_data['operators'], start=1):
            temp_providers[str(i)] = {"country_code": matched_ccode, "operator": operator}
            print(f"[{i}] {operator.title()}")
            
        while True:
            target_country, target_operator = select_provider(temp_providers)
            if not target_country or not target_operator:
                break  
                
            status = execute_polling_loop(target_country, target_operator)
            if status == "back_to_menu":
                return

def offline_search_menu():
    """Sub-menu for accessing offline data."""
    while True:
        print("\n" + "="*30)
        print("--- OFFLINE SEARCH MENU ---")
        print("[1] Search by Service Name")
        print("[2] Search by Country / Dial Code")
        print("[b] Go Back to Main Menu")
        
        choice = input("\n[?] Select an option: ").strip().lower()
        
        if choice == 'b':
            return
        elif choice == '1':
            service_offline_flow()
        elif choice == '2':
            country_offline_flow()
        else:
            print("[-] Invalid selection.")

def add_service_to_db():
    """Queries the live API for a service and MERGES it into the local JSON DB."""
    print("\n--- Add/Update Service in Database ---")
    while True:
        service_input = input("[?] Enter the new service name (e.g., 'netflix') or 'b' to go back: ").strip().lower()
        if service_input == 'b':
            return
        if not service_input:
            continue

        params = {
            "interval": "10min",
            "service": service_input,
            "token": TOKEN
        }

        print(f"[*] Querying live API on port {ACCESS_PORT} for '{service_input}'...")
        try:
            response = requests.get(ACCESS_INFO_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "Data retrieved successfully" and data.get("data"):
                raw_providers = data["data"]
                
                # Step 1: Deduplicate the incoming raw data to get clean fingerprints
                unique_incoming = {}
                for p in raw_providers:
                    key = f"{p['ccode'].lower()}_{p['operator'].lower().strip()}"
                    if key not in unique_incoming:
                        unique_incoming[key] = p
                
                # Step 2: Safely load the existing DB
                if os.path.exists(DB_FILE):
                    with open(DB_FILE, "r", encoding="utf-8") as f:
                        try:
                            db = json.load(f)
                        except json.JSONDecodeError:
                            db = {}
                else:
                    db = {}

                # Step 3: MERGE LOGIC - Only append new operators, never delete existing ones
                if service_input in db:
                    existing_providers = db[service_input]
                    
                    # Create a set of existing fingerprints so we don't add duplicates
                    existing_keys = {f"{p['ccode'].lower()}_{p['operator'].lower().strip()}" for p in existing_providers}
                    
                    added_count = 0
                    for key, p in unique_incoming.items():
                        if key not in existing_keys:
                            existing_providers.append(p)
                            existing_keys.add(key)
                            added_count += 1
                            
                    db[service_input] = existing_providers
                    print(f"[+] Merged! Added {added_count} new operators. Total stored operators for '{service_input}': {len(existing_providers)}.")
                else:
                    # If the service doesn't exist at all yet, just add the fresh list
                    db[service_input] = list(unique_incoming.values())
                    print(f"[+] Success! '{service_input}' newly saved to {DB_FILE} with {len(unique_incoming)} unique operators.")

                # Save back to disk
                with open(DB_FILE, "w", encoding="utf-8") as f:
                    json.dump(db, f, indent=4)

            else:
                print(f"[-] No active operators found for '{service_input}' right now. Database not updated.")

        except requests.exceptions.RequestException as e:
            print(f"[-] HTTP Error updating database: {e}")

if __name__ == "__main__":
    print("=== SMS OTP Automation Started ===")
    
    while True:
        print("\n" + "="*50)
        print("--- MAIN MENU ---")
        print("[1] Search by Service (Live API)")
        print("[2] Search Offline Database")
        print("[3] Add/Update a Service in Offline DB")
        print("[q] Quit")
        
        choice = input("\n[?] Select an option: ").strip().lower()
        
        if choice == 'q':
            print("[*] Exiting...")
            break
        elif choice == '1':
            service_live_flow()
        elif choice == '2':
            offline_search_menu()
        elif choice == '3':
            add_service_to_db()
        else:
            print("[-] Invalid selection. Please enter 1, 2, 3, or q.")