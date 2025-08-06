#!/usr/bin/env python3
"""
Simple web application with security vulnerabilities for demonstration
"""

from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (id, username, email, password) VALUES (1, 'admin', 'admin@example.com', 'password123')")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, email, password) VALUES (2, 'user', 'user@example.com', 'userpass')")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return '''
    <h1>Welcome to Vulnerable Web App</h1>
    <a href="/search">Search Users</a><br>
    <a href="/profile">View Profile</a>
    '''

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        # BUG 4: SQL Injection vulnerability
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        sql = f"SELECT username, email FROM users WHERE username LIKE '%{query}%'"
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()
        
        # BUG 5: XSS vulnerability - user input not escaped
        html = f"<h2>Search Results for: {query}</h2>"
        for user in results:
            html += f"<p>Username: {user[0]}, Email: {user[1]}</p>"
        return html
    else:
        return '''
        <form>
            <input type="text" name="q" placeholder="Search username...">
            <input type="submit" value="Search">
        </form>
        '''

@app.route('/profile')
def profile():
    user_id = request.args.get('id', '1')
    
    # BUG 6: Path traversal vulnerability
    filename = request.args.get('file', 'profile.txt')
    try:
        with open(f"profiles/{filename}", 'r') as f:
            content = f.read()
        return f"<h2>Profile Content:</h2><pre>{content}</pre>"
    except FileNotFoundError:
        return "Profile not found"

@app.route('/admin')
def admin():
    # BUG 7: No authentication check
    return '''
    <h2>Admin Panel</h2>
    <p>Secret admin functionality here!</p>
    <form action="/delete_user" method="post">
        <input type="text" name="user_id" placeholder="User ID to delete">
        <input type="submit" value="Delete User">
    </form>
    '''

if __name__ == '__main__':
    init_db()
    # BUG 8: Debug mode enabled in production
    app.run(debug=True, host='0.0.0.0', port=5000)