import subprocess

try:
    print("Running git push...")
    res = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    print(f"STDOUT: {res.stdout}")
    print(f"STDERR: {res.stderr}")
    print(f"Return Code: {res.returncode}")
except Exception as e:
    print(f"Error: {e}")
