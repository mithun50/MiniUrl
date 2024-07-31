import sqlite3
import string
import random

DATABASE = 'database.db'

def generate_short_code():
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for _ in range(6))
    return short_code

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def update_email_links(email):
    conn = get_db()
    c = conn.cursor()
    
    # Check if the email is already in the table
    c.execute('SELECT links_shortened FROM email_links WHERE email = ?', (email,))
    result = c.fetchone()
    
    if result:
        # Update the count if email already exists
        c.execute('UPDATE email_links SET links_shortened = links_shortened + 1 WHERE email = ?', (email,))
    else:
        # Insert a new record if email does not exist
        c.execute('INSERT INTO email_links (email, links_shortened) VALUES (?, 1)', (email,))
    
    conn.commit()
    conn.close()

def shorten_url(original_url, source, email=None):
    short_code = generate_short_code()
    
    conn = get_db()
    c = conn.cursor()
    
    # Insert the URL with the source
    c.execute('INSERT INTO urls (original_url, short_code, source) VALUES (?, ?, ?)', (original_url, short_code, source))
    
    # Update the email link count if an email is provided
    if email:
        update_email_links(email)
    
    conn.commit()
    conn.close()
    
    return short_code

def get_original_url(short_code):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT original_url FROM urls WHERE short_code = ?', (short_code,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return result[0]
    else:
        return None