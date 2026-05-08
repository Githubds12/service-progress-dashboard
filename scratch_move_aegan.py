import shutil
import os

src = r"c:\Users\Gorri\Documents\Reports\Aegan"
dst = r"c:\Users\Gorri\Documents\Reports\OldReports\Aegan_2026-05-08"

if os.path.exists(src):
    shutil.move(src, dst)
    print(f"Successfully moved {src} to {dst}")
else:
    print(f"Source {src} does not exist.")
