#!/usr/bin/env python3
"""
Simple script to test Google Cloud permissions without requiring Slack export data.
"""

import sys
from pathlib import Path

# Add the project to the path
sys.path.insert(0, str(Path(__file__).parent))

from slack_migrator.core.migrator import SlackToChatMigrator
from slack_migrator.utils.permissions import validate_permissions
from slack_migrator.utils.logging import setup_logger
import logging

def main():
    # Setup logger
    logger = setup_logger(verbose=True, debug_api=False, output_dir=None)

    print("=" * 60)
    print("Google Cloud Permissions Test")
    print("=" * 60)
    print()

    # Configuration
    creds_path = "slack-chat-migrator-sa-key.json"
    workspace_admin = "igo.shin@f-ship.jp"
    config_path = "test_config.yaml"
    export_path = "test_export"

    # Check if credentials file exists
    if not Path(creds_path).exists():
        print(f"[X] Error: Credentials file not found: {creds_path}")
        print("Please make sure the service account key file is in the correct location.")
        sys.exit(1)

    print(f"[*] Credentials file: {creds_path}")
    print(f"[*] Workspace admin: {workspace_admin}")
    print(f"[*] Config file: {config_path}")
    print(f"[*] Export path: {export_path} (dummy data for testing)")
    print()

    try:
        print("[*] Initializing migrator...")
        # Create a minimal migrator instance for permission testing
        migrator = SlackToChatMigrator(
            creds_path=creds_path,
            export_path=export_path,
            workspace_admin=workspace_admin,
            config_path=config_path,
            dry_run=True,
            verbose=True
        )

        print("[OK] Migrator initialized successfully")
        print()
        print("[*] Starting permission validation...")
        print("    This will create temporary test resources and clean them up.")
        print()

        # Run permission validation
        validate_permissions(migrator)

        print()
        print("=" * 60)
        print("[OK] SUCCESS! All permissions are configured correctly.")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. [OK] Google Cloud setup is complete")
        print("2. [ ]  Export your Slack data")
        print("3. [ ]  Create config.yaml file")
        print("4. [ ]  Run the migration")
        print()

        return 0

    except Exception as e:
        print()
        print("=" * 60)
        print("[X] PERMISSION CHECK FAILED")
        print("=" * 60)
        print()
        print(f"Error: {e}")
        print()
        print("Please review the errors above and:")
        print("1. Verify domain-wide delegation is set up correctly")
        print("2. Check that all required scopes are granted")
        print("3. Make sure the service account key file is correct")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
