# server.py
from flask import Flask, request, redirect, render_template, session, url_for, send_file
from shortener import get_original_url
from shortener import shorten_url
import sqlite3
import os
import bcrypt
import pytz
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()  # Use a secure key in production

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    if request.method == 'POST':
        original_url = request.form['original_url']
        short_code = shorten_url(original_url)
        short_url = url_for('redirect_url', short_code=short_code, _external=True)
    
    return render_template('index.html', short_url=short_url)
    
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
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM urls')
    total_links = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM telegram_users')
    total_users = c.fetchone()[0]
    c.execute('SELECT * FROM telegram_users')
    users = c.fetchall()
    conn.close()
    
    return render_template('admin_panel.html', total_links=total_links, total_users=total_users, users=users)

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

def start_flask():
    app.run(debug=True, use_reloader=False)  # Disable the reloader in a threaded environment

if __name__ == '__main__':
    start_flask()

