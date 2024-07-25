# add_admin.py
import sqlite3
import bcrypt

def add_admin(username, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Create the admins table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS admins (
        username TEXT PRIMARY KEY, 
        password TEXT)''')
    
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Insert the admin user
    try:
        c.execute('INSERT INTO admins (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        print(f"Admin user '{username}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"Admin user '{username}' already exists.")
    
    conn.close()

if __name__ == '__main__':
    # Replace with your desired username and password
    add_admin('admin', '@mithun#')

