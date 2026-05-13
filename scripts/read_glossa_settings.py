"""Read SMTP settings and notification recipients from glossa-lab database."""
import sqlite3

conn = sqlite3.connect(r'C:\Users\trist\Development\BitConcepts\glossa-lab\data\glossa.db')
keys = ['smtp_host', 'smtp_port', 'smtp_username', 'smtp_from', 'smtp_use_tls',
        'ms_graph_refresh_token', 'ms_graph_client_id', 'ms_graph_tenant_id']
rows = conn.execute(
    "SELECT key, value FROM settings WHERE key IN ({})".format(
        ','.join('?' for _ in keys)
    ), keys
).fetchall()
for k, v in rows:
    # Mask passwords/tokens
    if 'token' in k.lower() or 'password' in k.lower():
        print(f"{k} = [SET]")
    else:
        print(f"{k} = {v}")

recs = conn.execute(
    "SELECT email, label FROM notification_recipients WHERE active=1"
).fetchall()
for email, label in recs:
    print(f"RECIPIENT: {email}  ({label})")
conn.close()
