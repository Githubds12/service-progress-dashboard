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
    
    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Initiating dashboard update...")
        
        try:
            # Run the update script
            result = subprocess.run([sys.executable, update_script], 
                                 cwd=project_root, 
                                 capture_output=True, 
                                 text=True)
            
            if result.returncode == 0:
                print(f"[{current_time}] Success: Dashboard updated and pushed to GitHub/Render.")
            else:
                print(f"[{current_time}] Error in update_dashboard.py:\n{result.stderr}")
                
        except Exception as e:
            print(f"[{current_time}] System Error: {e}")
        
        # Wait for 2 minutes
        time.sleep(2 * 60)

if __name__ == "__main__":
    main()
