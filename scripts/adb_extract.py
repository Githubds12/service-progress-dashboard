import subprocess
import re
import sys
import os

def get_device_id():
    output = subprocess.run('adb devices', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True).stdout.strip()
    lines = output.split('\n')[1:] # Skip header
    devices = [line.split('\t')[0] for line in lines if line.strip() and '\tdevice' in line]
    return devices[0] if devices else None

def run_cmd(cmd):
    device_id = get_device_id()
    if device_id:
        cmd = cmd.replace('adb ', f'adb -s {device_id} ')
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    return result.stdout.strip()

def search_installed_packages(keyword):
    output = run_cmd('adb shell pm list packages')
    packages = [line.replace('package:', '').strip() for line in output.split('\n') if line.strip()]
    matches = [p for p in packages if keyword.lower() in p.lower()]
    return matches

def get_package_version(package_name):
    output = run_cmd(f'adb shell dumpsys package {package_name}')
    match = re.search(r'versionName=([^\s]+)', output)
    if match:
        return match.group(1)
    return "Unknown"

def main():
    if len(sys.argv) < 3:
        print("Usage: python adb_extract.py <path_to_inf_txt> <app_keyword>")
        print("Example: python adb_extract.py \"c:\\Users\\Gorri\\Documents\\Reports\\BetJam\\inf.txt\" betjam")
        sys.exit(1)
        
    inf_path = sys.argv[1]
    keyword = sys.argv[2]
    
    if not os.path.exists(inf_path):
        print(f"[-] inf.txt not found at: {inf_path}")
        sys.exit(1)
        
    print(f"[*] Searching installed packages for '{keyword}'...")
    matches = search_installed_packages(keyword)
    
    if not matches:
        print(f"[-] No packages found matching '{keyword}'.")
        sys.exit(1)
        
    if len(matches) > 1:
        print(f"[-] Multiple packages matched '{keyword}':")
        for m in matches:
            print(f"    - {m}")
        print("Please provide a more specific keyword.")
        sys.exit(1)
        
    package_name = matches[0]
    print(f"[+] Found Package: {package_name}")
    
    version = get_package_version(package_name)
    print(f"[+] Found Version: {version}")
    
    # Write to inf.txt
    with open(inf_path, 'a', encoding='utf-8') as f:
        f.write(f"\nPackage Name: {package_name}\nVersion: {version}\n")
        
    print(f"[+] Successfully appended to {inf_path}")

if __name__ == "__main__":
    main()
