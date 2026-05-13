"""List tables and find notification/settings tables in glossa-lab DB."""
import sqlite3

conn = sqlite3.connect(r'C:\Users\trist\Development\BitConcepts\glossa-lab\data\glossa.db')
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
print("Tables:", [t[0] for t in tables])

# Try to find any settings-like or notification-like tables
for t in tables:
    name = t[0]
    if any(kw in name.lower() for kw in ['setting', 'notif', 'recipient', 'email', 'config']):
        print(f"\nTable: {name}")
        cols = conn.execute(f"PRAGMA table_info({name})").fetchall()
        print("  Columns:", [c[1] for c in cols])
        rows = conn.execute(f"SELECT * FROM {name} LIMIT 5").fetchall()
        for r in rows:
            # mask potential secrets
            masked = []
            for i, v in enumerate(r):
                col_name = cols[i][1].lower()
                if any(k in col_name for k in ['password', 'token', 'secret', 'key']):
                    masked.append('[MASKED]')
                else:
                    masked.append(str(v)[:80])
            print(" ", masked)
conn.close()
