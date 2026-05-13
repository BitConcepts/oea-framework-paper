"""Read notification recipients and locate SMTP config in glossa-lab."""
import sqlite3, os, glob

db_path = r'C:\Users\trist\Development\BitConcepts\glossa-lab\data\glossa.db'
conn = sqlite3.connect(db_path)

# Recipients
recs = conn.execute(
    "SELECT email, label, active FROM notification_recipients"
).fetchall()
print("Recipients:")
for r in recs:
    print(f"  {r[2]} | {r[0]} | {r[1]}")

# Check if app_settings or config table exists elsewhere
data_dir = r'C:\Users\trist\Development\BitConcepts\glossa-lab\data'
print("\nFiles in data dir:")
for f in os.listdir(data_dir):
    print(f"  {f}")

# Look for any config/settings file
print("\nOther config files:")
for pattern in ['*.json', '*.env', '*.cfg', '*.ini', '*.yaml']:
    for f in glob.glob(os.path.join(r'C:\Users\trist\Development\BitConcepts\glossa-lab', pattern)):
        print(f"  {f}")

conn.close()
