import os
import sys
import requests
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, redirect, url_for, session, Response

# 1. Setup Flask with Absolute Path to fix the "TemplateNotFound" error
# This tells Flask exactly where your 'templates' folder is on your Desktop
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = "beast_scanner_ultra_secret"

# 2. Path helper for future Desktop App packaging
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 3. Temporary Operator Database
users = {"admin": "password123"}

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    ip_data = None
    if request.method == 'POST':
        target_ip = request.form.get('ip_address')
        try:
            # Fetching live geolocation data for the radar
            response = requests.get(f"http://ip-api.com/json/{target_ip}")
            ip_data = response.json()
        except:
            ip_data = {"status": "fail"}
            
    return render_template('index.html', data=ip_data, user=session['user'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        users[u] = p
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/download/<platform>')
def download_app(platform):
    # This delivers a placeholder image for now as requested
    img_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQXEy72AUROHF37SEjph2ZjkFiwyQhoeaE8nw&s"
    img_data = requests.get(img_url).content
    return Response(
        img_data,
        headers={
            "Content-Disposition": f"attachment; filename=Beast_Scanner_{platform}.jpg",
            "Content-Type": "image/jpeg"
        }
    )

def open_browser():
    # Opens your specific project port automatically
    webbrowser.open_new("http://127.0.0.1:5002/register")

if __name__ == '__main__':
    # Start the browser 1.5 seconds after the server begins
    Timer(1.5, open_browser).start()
    # Port 5002 avoids conflict with your old QR project
    app.run(host='0.0.0.0', port=5002, debug=True)