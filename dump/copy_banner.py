import shutil
import os

src = r"C:\Users\Gorri\.gemini\antigravity\brain\2f59677d-7aa1-4a6c-8e52-36101a193380\dynamic_productivity_banner_png_1777276790940.png"
dst = r"c:\Users\Gorri\Documents\Reports\productivity_banner.png"

if os.path.exists(src):
    shutil.copy(src, dst)
    print(f"Copied to {dst}")
else:
    print(f"Source not found: {src}")
