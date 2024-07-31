import sqlite3

def setup_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Create table for URLs
    c.execute('''CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY, 
        original_url TEXT, 
        short_code TEXT,
        source TEXT)''')
    
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
    
    # Create table for email addresses and the count of links shortened per email
    c.execute('''CREATE TABLE IF NOT EXISTS email_links (
        email TEXT PRIMARY KEY, 
        links_shortened INTEGER DEFAULT 0)''')
    

    # Create table for email link counts
    c.execute('''CREATE TABLE IF NOT EXISTS email_link_counts (
        email TEXT PRIMARY KEY, 
        link_count INTEGER DEFAULT 0)''')
    
    conn.commit()
    conn.close()



if __name__ == '__main__':
    setup_database()