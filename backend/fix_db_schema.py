import sqlite3

def add_columns():
    conn = sqlite3.connect('sql_app.db')
    cursor = conn.cursor()
    try:
        print("Adding created_at column...")
        cursor.execute('ALTER TABLE users ADD COLUMN created_at DATETIME')
    except sqlite3.OperationalError as e:
        print(f"created_at could not be added (maybe already exists): {e}")
        
    try:
        print("Adding updated_at column...")
        cursor.execute('ALTER TABLE users ADD COLUMN updated_at DATETIME')
    except sqlite3.OperationalError as e:
        print(f"updated_at could not be added (maybe already exists): {e}")
        
    conn.commit()
    conn.close()
    print("Database modification completed.")

if __name__ == "__main__":
    add_columns()
