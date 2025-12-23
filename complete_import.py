"""
Complete import for Google Chat spaces and add members.
"""
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuration
CREDS_PATH = r"c:\Users\覃惟剛\Desktop\slack-chat-migrator\slack-to-gchat-migration-eefc572d7e9d.json"
WORKSPACE_ADMIN = "igo.shin@f-ship.jp"
SPACE_ID = "spaces/AAQA6CIcvrk"

REQUIRED_SCOPES = [
    "https://www.googleapis.com/auth/chat.import",
    "https://www.googleapis.com/auth/chat.spaces",
    "https://www.googleapis.com/auth/chat.messages",
    "https://www.googleapis.com/auth/chat.spaces.readonly",
    "https://www.googleapis.com/auth/chat.memberships.readonly",
    "https://www.googleapis.com/auth/drive",
]

def get_chat_service():
    """Initialize Google Chat API service."""
    creds = service_account.Credentials.from_service_account_file(
        CREDS_PATH, scopes=REQUIRED_SCOPES
    )
    delegated = creds.with_subject(WORKSPACE_ADMIN)
    return build('chat', 'v1', credentials=delegated)

def complete_import(space_id):
    """Complete import for a space."""
    chat = get_chat_service()

    try:
        print(f"Completing import for space: {space_id}")
        result = chat.spaces().completeImport(name=space_id).execute()
        print(f"[OK] Import completed successfully!")
        print(f"Space details: {result}")
        return True
    except Exception as e:
        print(f"[ERROR] Error completing import: {e}")
        return False

def add_member(space_id, user_email):
    """Add a member to the space."""
    chat = get_chat_service()

    try:
        print(f"Adding member {user_email} to space...")
        member_body = {
            "member": {
                "name": f"users/{user_email}",
                "type": "HUMAN"
            }
        }
        result = chat.spaces().members().create(
            parent=space_id,
            body=member_body
        ).execute()
        print(f"[OK] Member added successfully!")
        return True
    except Exception as e:
        if "409" in str(e):
            print(f"[OK] Member already exists in space")
            return True
        else:
            print(f"[ERROR] Error adding member: {e}")
            return False

def main():
    print("=" * 60)
    print("Google Chat Space Import Completion Tool")
    print("=" * 60)

    # Step 1: Complete import
    print("\nStep 1: Completing space import...")
    if not complete_import(SPACE_ID):
        print("\n⚠️ Import completion failed. The space might already be completed.")
        print("Continuing to add members...\n")

    # Step 2: Add admin as member
    print("\nStep 2: Adding workspace admin as member...")
    add_member(SPACE_ID, WORKSPACE_ADMIN)

    print("\n" + "=" * 60)
    print("[OK] Process completed!")
    print(f"Space URL: https://chat.google.com/room/AAQA6CIcvrk")
    print("=" * 60)

if __name__ == "__main__":
    main()
