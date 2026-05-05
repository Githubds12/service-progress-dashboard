import shutil
import os

src_dir = r'C:\Users\Gorri\Desktop\devi'
dest_dir = r'c:\Users\Gorri\Documents\Reports\dashboard'

mapping = {
    'WhatsApp Image 2026-05-05 at 9.17.41 PM (2).jpeg': 'bhairavi_1.jpg',
    'WhatsApp Image 2026-05-05 at 9.17.39 PM.jpeg': 'bhairavi_2.jpg',
    'WhatsApp Image 2026-05-05 at 9.17.53 PM (1).jpeg': 'bhairavi_3.jpg',
    'WhatsApp Image 2026-05-05 at 9.17.58 PM.jpeg': 'bhairavi_4.jpg'
}

for src_name, dest_name in mapping.items():
    src_path = os.path.join(src_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    try:
        shutil.copy2(src_path, dest_path)
        print(f"Copied {src_name} to {dest_name}")
    except Exception as e:
        print(f"Error copying {src_name}: {e}")
