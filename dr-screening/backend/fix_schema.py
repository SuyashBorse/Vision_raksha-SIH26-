"""Fix SQLite CHECK constraint: add 'asha' to users.role constraint.
SQLite doesn't support ALTER CONSTRAINT, so we recreate the table."""
import sqlite3

conn = sqlite3.connect("retinai.db")
cur = conn.cursor()

# Get current schema
cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users'")
row = cur.fetchone()
if row:
    print("Current schema:")
    print(row[0])
    print()

# Check if 'asha' is already in the constraint
if row and "'asha'" not in row[0]:
    print("'asha' role is MISSING from CHECK constraint. Fixing...")
    
    # Get existing data
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    print(f"Found {len(users)} existing users to preserve")
    
    # Rename old table
    cur.execute("ALTER TABLE users RENAME TO users_old")
    
    # Recreate with correct constraint (including 'asha' and UNIQUE on username)
    cur.execute("""
        CREATE TABLE users (
            id VARCHAR(20) NOT NULL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role VARCHAR(20) NOT NULL DEFAULT 'asha' CHECK(role IN ('asha','doctor','field_worker','officer','admin')),
            phc_id VARCHAR(20) REFERENCES phcs(id),
            created_at DATETIME,
            is_active INTEGER DEFAULT 1,
            username TEXT UNIQUE
        )
    """)
    
    # Restore data
    if users:
        placeholders = ",".join(["?"] * len(col_names))
        cols = ",".join(col_names)
        cur.executemany(f"INSERT INTO users ({cols}) VALUES ({placeholders})", users)
        print(f"Restored {len(users)} users")
    
    # Drop old table
    cur.execute("DROP TABLE users_old")
    
    conn.commit()
    print("DONE - CHECK constraint fixed!")
    
    # Verify
    cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users'")
    print("\nNew schema:")
    print(cur.fetchone()[0])
else:
    print("'asha' role already present in CHECK constraint. No fix needed.")

conn.close()
