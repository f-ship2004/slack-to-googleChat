
import os
import unicodedata
from pathlib import Path

export_path = Path("/Users/shinigo/Desktop/slack-chat-migrator/slack_chanel_data")
# Find the NFD directory again
nfd_name = None
for item in export_path.iterdir():
    if "引継" in unicodedata.normalize('NFC', item.name):
        nfd_name = item.name
        break

if not nfd_name:
    print("Directory not found")
    exit(1)

nfc_name = unicodedata.normalize('NFC', nfd_name)
print(f"Original (NFD): {ascii(nfd_name)}")
print(f"Normalized (NFC): {ascii(nfc_name)}")

nfc_path = export_path / nfc_name
print(f"Trying to access: {nfc_path}")
print(f"Exists? {nfc_path.exists()}")
print(f"Is Dir? {nfc_path.is_dir()}")

try:
    subfiles = list(nfc_path.iterdir())
    print(f"Success! Found {len(subfiles)} files inside.")
except Exception as e:
    print(f"Failed to list directory: {e}")
