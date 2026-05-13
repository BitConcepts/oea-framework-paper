"""List keys in .keys.json (masks values) and show smtp/email related ones."""
import json

try:
    with open(r'C:\Users\trist\Development\BitConcepts\glossa-lab\data\.keys.json') as f:
        keys_data = json.load(f)
    print("Keys present:", list(keys_data.keys()))
    smtp_keys = {k: ('[SET]' if v else '[EMPTY]')
                 for k, v in keys_data.items()
                 if any(kw in k.lower() for kw in ['smtp', 'email', 'mail', 'graph', 'notif'])}
    print("Email/SMTP keys:", smtp_keys)
    # Also show any recipient-like entry
    for k, v in keys_data.items():
        if '@' in str(v):
            print(f"Possible email address in key '{k}'")
except FileNotFoundError:
    print(".keys.json not found")
except Exception as e:
    print(f"Error: {e}")
