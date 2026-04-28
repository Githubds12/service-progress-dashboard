import os
import sys
import glob
from playwright.sync_api import sync_playwright

# Credentials based on C:\HTB-Notes-Portal\SyncAndFixDatabase.py
EMAIL = "deepanshu@test.com"
PASS = "deep@nshu"
UI_BASE = "http://51.195.24.179:3000"
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

def get_service_name(folder_path):
    inf_file = os.path.join(folder_path, "inf.txt")
    if os.path.exists(inf_file):
        with open(inf_file, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            if first_line:
                # Extract just the first word (usually the service name before [UUID])
                name = first_line.split()[0]
                return name
    return input("Enter service name to search: ").strip()

def get_app_details(folder_path):
    sheet_file = os.path.join(folder_path, "googlesheet.txt")
    if os.path.exists(sheet_file):
        with open(sheet_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith(("Date:", "Service", "Host", "Verification", "Captcha", "Encryption", "Rate", "Endpoint", "Bot", "Flow", "Proof", "Researcher", "com.google")):
                    parts = line.split()
                    if len(parts) >= 2:
                        return parts[0], parts[1]
    return "", ""

def main():
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = os.getcwd()
        if not os.path.exists(os.path.join(folder_path, "inf.txt")):
            user_input = input(f"Enter the folder path containing inf.txt (default is current directory): ")
            if user_input.strip():
                folder_path = user_input.strip()

    service_name = get_service_name(folder_path)
    app_url, app_version = get_app_details(folder_path)
    print(f"[*] Targeting Service: {service_name}")
    print(f"[*] Extracted App URL: {app_url}, Version: {app_version}")
    
    # Locate report and har files
    har_files = glob.glob(os.path.join(folder_path, "*.har"))
    report_files = glob.glob(os.path.join(folder_path, "*report.md"))
    
    report_file = None
    for r in report_files:
        if "automation" not in r.lower() and "vulnerability" not in r.lower():
            report_file = r
            break
    if not report_file and report_files:
        report_file = report_files[0]
    
    print(f"[*] Found {len(har_files)} HAR files.")
    if report_file:
        print(f"[*] Found Report: {os.path.basename(report_file)}")
    else:
        print("[-] No report.md found!")

    with sync_playwright() as p:
        print("[*] Connecting to the running Brave Browser...")
        try:
            # Connect to the actively running browser over CDP
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            
            # Open a new page/tab so it's visible and doesn't hijack an active session
            page = context.new_page()
                
            print("[+] Successfully connected to browser!")
        except Exception as e:
            print("[-] Could not connect to Brave. Ensure you started it with --remote-debugging-port=9222")
            print(f"Error details: {e}")
            return
        
        # 1. Login
        print(f"[*] Navigating to {UI_BASE}/login")
        try:
            page.goto(f"{UI_BASE}/login", timeout=60000, wait_until="domcontentloaded")
        except Exception as e:
            print(f"[-] Page load timeout, trying to proceed anyway: {e}")
        
        # Trying standard selectors for login form
        try:
            page.wait_for_selector("input[type='email']", timeout=10000)
            page.fill("input[type='email']", EMAIL)
            page.fill("input[type='password']", PASS)
            page.click("button[type='submit'], button:has-text('Login'), button:has-text('Sign In')")
            print("[+] Filled login details.")
        except Exception as e:
            print(f"[-] Could not auto-fill login: {e}")
            print("[*] Please complete login manually in the browser window.")
        
        # Wait for navigation to complete - usually token is set and redirects
        try:
            # It usually redirects to /dashboard or /services
            page.wait_for_url("**/*", timeout=5000)
        except Exception:
            pass # Ignore wait timeouts here, we will explicitly navigate to /services next
        
        print("[+] Login check complete, moving to services...")
        
        # 2. Go to services page
        try:
            page.goto(f"{UI_BASE}/services", timeout=60000, wait_until="domcontentloaded")
        except Exception as e:
            print(f"[-] Page load timeout for services, trying to proceed: {e}")
        
        # 3. Search for the feature/service
        print(f"[*] Searching for '{service_name}'...")
        try:
            # Type into any typical search input
            search_input = page.wait_for_selector("input[type='search'], input[placeholder*='search' i], input[placeholder*='Search' i]", timeout=10000)
            search_input.fill(service_name)
            page.keyboard.press("Enter")
            page.wait_for_timeout(2000)  # brief wait for results to load
        except Exception as e:
            print("[-] Could not find search bar. You may need to search manually.")
            
        # 4. Click on the service name
        print(f"[*] Clicking on '{service_name}'...")
        try:
            # Matches case-insensitive text
            link = page.get_by_text(service_name, exact=True)
            if link.count() > 0:
                link.first.click()
            else:
                # If exact text fails, try looser match
                page.locator(f"text={service_name}").first.click()
            page.wait_for_load_state('networkidle')
        except Exception as e:
            print("[-] Could not automatically click the service. Please click it in the browser.")
            
        # 5. Click Android Claim button specifically
        print("[*] Clicking Android Claim button...")
        try:
            page.wait_for_timeout(2000)
            
            # Try to find a Claim button inside a container that also contains the word 'Android'
            # Or fall back to letting the user click it to avoid clicking 'Web' by accident
            android_claim = page.locator("tr:has-text('Android') button:has-text('Claim'), div:has-text('Android') button:has-text('Claim')").first
            
            if android_claim.is_visible():
                android_claim.click()
                print("[+] Auto-clicked Android Claim button.")
                page.wait_for_load_state('networkidle')
            else:
                print("[-] Could not reliably identify the *Android* specific Claim button.")
                print("[-] Pausing auto-click to prevent picking Web/iOS by mistake. Please click 'Claim' manually!")
        except Exception:
            print("[-] Error attempting to auto-click the Android Claim button. Please click manually.")
            
        # 6. Upload files
        print("[*] Uploading files...")
        try:
            # Usually the report is the primary file input, HARs in a second one, 
            # or they are combined. We will try to assign them to inputs if found.
            file_inputs = page.locator("input[type='file']")
            count = file_inputs.count()
            
            if count >= 1 and report_file:
                # Assume first is Report
                print("[+] Uploading Report...")
                file_inputs.nth(0).set_input_files(report_file)
            
            if count >= 2 and har_files:
                # Assume second is HAR data
                print("[+] Uploading HAR files...")
                file_inputs.nth(1).set_input_files(har_files)
            elif count == 1 and har_files and not report_file:
                # Only 1 input, maybe just data
                file_inputs.nth(0).set_input_files(har_files)
                
        except Exception as e:
            print(f"[-] Could not map file uploads automatically: {e}")

        # 7. Auto-fill Source/URL and Version
        print("[*] Auto-filling Source/URL and Version...")
        try:
            if app_url:
                source_input = page.locator("input[placeholder*='source' i], input[placeholder*='url' i], input[name*='source' i], input[name*='url' i], input[placeholder*='Source' i], input[placeholder*='URL' i]").first
                if source_input.is_visible():
                    source_input.fill(app_url)
            
            if app_version:
                version_input = page.locator("input[placeholder*='version' i], input[name*='version' i], input[placeholder*='Version' i]").first
                if version_input.is_visible():
                    version_input.fill(app_version)
                    
            print("[+] Filled App details.")
        except Exception as e:
            print(f"[-] Could not auto-fill app details: {e}")

        # 8. Auto-click Submit/Confirm Claim
        print("[*] Confirming claim...")
        try:
            submit_btn = page.locator("button:has-text('Submit'), button:has-text('Save'), button:has-text('Confirm'), button:has-text('Claim')").last
            if submit_btn.is_visible():
                submit_btn.click()
                print("[+] Auto-clicked Submit/Confirm/Claim.")
                page.wait_for_timeout(2000)
                page.wait_for_load_state('networkidle')
            else:
                print("[-] Could not find the Confirm/Submit button.")
        except Exception as e:
            print(f"[-] Could not auto-click Submit: {e}")

        print("\n" + "="*50)
        print("[+] AUTOMATION COMPLETE")
        print("All automated steps are complete. The browser will stay open briefly so you can see.")
        print("="*50 + "\n")
        
        page.wait_for_timeout(3000)
        browser.close()

if __name__ == '__main__':
    main()
