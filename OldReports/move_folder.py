import shutil
import os

src = "OpenTable"
dst = "OldReports/OpenTable"

try:
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.move(src, dst)
    print("SUCCESS")
except Exception as e:
    print(f"ERROR: {e}")
