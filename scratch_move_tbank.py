import shutil
import os

src = r"c:\Users\Gorri\Documents\Reports\Tbank"
dst = r"c:\Users\Gorri\Documents\Reports\OldReports\Tbank_2026-05-08"

if os.path.exists(src):
    shutil.move(src, dst)
    print(f"Successfully moved {src} to {dst}")
else:
    print(f"Source {src} does not exist.")
