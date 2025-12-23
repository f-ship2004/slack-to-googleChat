#!/usr/bin/env python3
import yaml

# Load the report
with open('migration_logs/run_20251218_160458/migration_report.yaml', encoding='utf-8') as f:
    report = yaml.safe_load(f)

# Get users
users = report.get('users', {})
print(f'Total users in report: {len(users)}')

# Categorize users
has_email = [u for u in users.values() if u.get('email')]
no_email = [u for u in users.values() if not u.get('email')]
is_bot = [u for u in users.values() if u.get('is_bot')]
real_users_no_email = [u for u in no_email if not u.get('is_bot')]

print(f'\nUser categories:')
print(f'  Users with email: {len(has_email)}')
print(f'  Users without email: {len(no_email)}')
print(f'  Bots: {len(is_bot)}')
print(f'  Real users without email: {len(real_users_no_email)}')

print(f'\nFirst 15 real users without email:')
for i, u in enumerate(real_users_no_email[:15]):
    print(f'  {i+1}. {u.get("display_name", "N/A")} (ID: {u.get("slack_id", "N/A")})')

# Check recommendations
recs = report.get('recommendations', {})
print(f'\nRecommendations:')
for key, value in recs.items():
    print(f'  {key}: {value}')
