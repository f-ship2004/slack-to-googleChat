"""
Analyze image files in Slack export
"""
import json
import glob
import os

slack_data_path = r"C:\Users\覃惟剛\Desktop\slack-chat-migrator\slack_chanel_data\unit-情シス"
json_files = glob.glob(os.path.join(slack_data_path, "2025-*.json"))

total_images = 0
image_info = []

for json_file in json_files[:5]:  # Check first 5 files
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            messages = json.load(f)

        for msg in messages:
            if not isinstance(msg, dict):
                continue

            files = msg.get('files', [])
            for file_obj in files:
                mimetype = file_obj.get('mimetype', '')
                if mimetype.startswith('image/'):
                    total_images += 1
                    image_info.append({
                        'name': file_obj.get('name', 'unknown'),
                        'mimetype': mimetype,
                        'size': file_obj.get('size', 0),
                        'url': file_obj.get('url_private', 'N/A')[:80]
                    })
    except Exception as e:
        print(f"Error processing {json_file}: {e}")

print(f"\n=== Image Analysis ===")
print(f"Total images found: {total_images}")
print(f"\nFirst 10 images:")
for i, img in enumerate(image_info[:10], 1):
    print(f"{i}. {img['name']}")
    print(f"   Type: {img['mimetype']}, Size: {img['size']/1024:.1f} KB")
    print(f"   URL: {img['url']}...")
    print()
