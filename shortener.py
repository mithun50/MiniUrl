# shortener.py
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

def shorten_url(original_url):
    short_code = generate_short_code()
    
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO urls (original_url, short_code) VALUES (?, ?)', (original_url, short_code))
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

