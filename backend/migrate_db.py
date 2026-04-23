import sqlite3
import os

db_path = "C:/Users/ASUS/Desktop/AgroCure AI/backend/sql_app.db"

def migrate():
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Checking for new columns...")
    
    try:
        # Add is_verified column
        cursor.execute("ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT 0")
        print("Added is_verified column.")
    except sqlite3.OperationalError:
        print("is_verified column already exists.")

    try:
        # Add verification_code column
        cursor.execute("ALTER TABLE users ADD COLUMN verification_code TEXT")
        print("Added verification_code column.")
    except sqlite3.OperationalError:
        print("verification_code column already exists.")

    conn.commit()
    conn.close()
    print("Migration complete!")

if __name__ == "__main__":
    migrate()
