# setup_database.py
import sqlite3

def setup_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Create table for URLs
    c.execute('''CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY, 
        original_url TEXT, 
        short_code TEXT)''')
    
    # Create table for admin users
    c.execute('''CREATE TABLE IF NOT EXISTS admins (
        username TEXT PRIMARY KEY, 
        password TEXT)''')
    
    # Create table for Telegram users with timestamp
    c.execute('''CREATE TABLE IF NOT EXISTS telegram_users (
        user_id INTEGER PRIMARY KEY, 
        username TEXT, 
        full_name TEXT, 
        links_shortened INTEGER DEFAULT 0, 
        last_visited TEXT)''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()

