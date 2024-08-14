from flask import Flask, request, redirect, render_template, session, url_for, send_file, flash
from shortener import get_original_url, shorten_url
import sqlite3
import os
import bcrypt
import pytz
from datetime import datetime
from contextlib import closing
import re
import requests
from flask_cors import CORS 
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)
app.secret_key = os.urandom(24).hex() 
# Use a secure key in production


CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow all origins for API routes

# Helper function to validate email addresses
def is_valid_url(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException:
        return False

from email_validator import validate_email, EmailNotValidError

def is_valid_email(email):
    try:
        # Validate email
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


def is_valid_urli(url):
    # Ensure the URL starts with http or https and is reachable
    return url.startswith(('http://', 'https://')) 

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    error_message = None
    success_message = None
 
    if request.method == 'POST':
        original_url = request.form['original_url']
        email = request.form.get('email')

        if not is_valid_email(email):
            error_message = "Invalid email address."
        elif not is_valid_url(original_url):
            error_message = "The URL is not valid or NotReachable."
        elif not is_valid_urli(original_url):
                    
          error_message = "Your Url is Invalid or http:// or https:// . is not Present"
        else:
            short_code = shorten_url(original_url, 'website')
            short_url = url_for('redirect_url', short_code=short_code, _external=True)

            # Store email and link count in the database
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('INSERT OR IGNORE INTO email_link_counts (email) VALUES (?)', (email,))
            c.execute('UPDATE email_link_counts SET link_count = link_count + 1 WHERE email = ?', (email,))
            conn.commit()
            conn.close()

            success_message = "Shortened URL Created Successfully"
    
    return render_template('index.html', short_url=short_url, error_message=error_message, success_message=success_message)
    
    

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contactus')
def contact():
    return render_template('contactus.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT password FROM admins WHERE username = ?', (username,))
        stored_password = c.fetchone()
        conn.close()
        
        if stored_password and bcrypt.checkpw(password.encode('utf-8'), stored_password[0]):
            session['username'] = username
            return redirect(url_for('admin_panel'))
        return 'Invalid credentials', 401
    
    return render_template('login.html')

@app.route('/admin')
def admin_panel():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    with closing(sqlite3.connect('database.db')) as conn:
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM urls WHERE source = ?', ('website',))
        total_links_website = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM urls WHERE source = ?', ('bot',))
        total_links_bot = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM telegram_users')
        total_users = c.fetchone()[0]
        c.execute('SELECT * FROM telegram_users')
        users = c.fetchall()
        c.execute('SELECT * FROM email_link_counts')
        email_counts = c.fetchall()
    
    return render_template('admin_panel.html', total_links_website=total_links_website, total_links_bot=total_links_bot, total_users=total_users, users=users, email_counts=email_counts)

@app.route('/download_db')
def download_db():
    db_file = 'database.db'
    txt_file = 'database.txt'
    
    # Export the database to a text file
    conn = sqlite3.connect(db_file)
    with open(txt_file, 'w') as f:
        for line in conn.iterdump():
            f.write(f'{line}\n')
    conn.close()
    
    return send_file(txt_file, as_attachment=True, download_name='database.txt')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/<short_code>')
def redirect_url(short_code):
    original_url = get_original_url(short_code)
    
    if original_url:
        return redirect(original_url)
    else:
        return 'URL not found', 404
@app.route('/api/shorten', methods=['POST'])
def api_shorten_url():
    data = request.json
    original_url = data.get('longUrl')

    if not original_url:
        return jsonify({'error': 'No long URL provided'}), 400

    short_code = shorten_url(original_url, 'website')
    short_url = url_for('redirect_url', short_code=short_code, _external=True)

    return jsonify({'shortUrl': short_url})










def start_flask():
    app.run(host="0.0.0.0", port=8000, debug=True, use_reloader=False)  # Disable the reloader in a threaded environment

if __name__ == '__main__':
    start_flask()
