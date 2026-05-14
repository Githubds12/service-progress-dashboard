import time
import subprocess
import os
import sys

def main():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    update_script = os.path.join(script_dir, "update_dashboard.py")
    
    print(f"--- Dashboard Auto-Sync Started (Every 15 Minutes) ---")
    print(f"Project Root: {project_root}")
    
    # Ensure dashboard dir exists for logging
    dash_dir = os.path.join(project_root, "dashboard")
    if not os.path.exists(dash_dir):
        os.makedirs(dash_dir)

    log_file = os.path.join(dash_dir, "sync.log")
    status_file = os.path.join(dash_dir, "last_sync.json")

    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Initiating dashboard update...")
        
        with open(log_file, "a") as f:
            f.write(f"[{current_time}] SYNC_START: Initiating update...\n")

        try:
            # Run the update script
            result = subprocess.run([sys.executable, update_script], 
                                 cwd=project_root, 
                                 capture_output=True, 
                                 text=True)
            
            status = "SUCCESS" if result.returncode == 0 else "ERROR"
            msg = "Dashboard updated and pushed." if result.returncode == 0 else f"Error: {result.stderr[:200]}"
            
            with open(log_file, "a") as f:
                f.write(f"[{current_time}] SYNC_RESULT: {status} - {msg}\n")
            
            # Write heartbeat for dashboard
            with open(status_file, "w") as f:
                json.dump({
                    "last_sync": current_time,
                    "status": status,
                    "message": msg
                }, f, indent=2)

            if result.returncode == 0:
                print(f"[{current_time}] Success: Dashboard updated.")
            else:
                print(f"[{current_time}] Error: Check sync.log")
                
        except Exception as e:
            error_msg = f"System Error: {e}"
            print(f"[{current_time}] {error_msg}")
            with open(log_file, "a") as f:
                f.write(f"[{current_time}] SYNC_FATAL: {error_msg}\n")
        
        # Wait for 15 minutes
        time.sleep(15 * 60)

if __name__ == "__main__":
    main()
