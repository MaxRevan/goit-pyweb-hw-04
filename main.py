import socket
import threading
import json
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs


HTTP_PORT = 3000
SOCKET_PORT = 5000
STORAGE_DIR = 'storage'
DATA_FILE = 'storage/data.json'


class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
            print(f"Завантаження: {self.path}")
        elif self.path == '/message.html':
            self.path = 'message.html'
            print(f"Завантаження: {self.path}")
        elif self.path == '/logo.png':
            self.path = 'logo.png'
            print(f"Завантаження: {self.path}")
        elif self.path == '/style.css':
            self.path = 'style.css'
            print(f"Завантаження: {self.path}")
        else:
            self.path = '/error.html'
            self.send_response(404)
            self.end_headers()
            print(f"Завантаження: {self.path}")
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = parse_qs(post_data.decode('utf-8'))
            username = params['username'][0]
            message_text = params['message'][0]
            data = {'username': username, 'message': message_text}
            
            send_to_socket_server(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Message Sent")
        else:
            self.send_error(404, "Page Not Found")


def send_to_socket_server(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = json.dumps(data).encode('utf-8')
    client_socket.sendto(message, ('127.0.0.1', SOCKET_PORT))
    client_socket.close()

def socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', SOCKET_PORT))
    message, address = server_socket.recvfrom(1024)
    data = json.loads(message.decode('utf-8'))
    timestamp = str(datetime.now())
    try:
        with open(DATA_FILE, 'r') as file:
            current_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        current_data = {}
    current_data[timestamp] = data
    with open(DATA_FILE, 'w') as file:
        json.dump(current_data, file, indent=4)


def setup_storage():
    try:
        with open(DATA_FILE, 'r') as file:
            pass  
    except FileNotFoundError:
        try:
            with open(DATA_FILE, 'w') as file:
                json.dump({}, file)
            print(f"Файл {DATA_FILE} створено.")
        except FileNotFoundError:
            with open('storage/data.json', 'w') as file:
                json.dump({}, file)
            print("Директорія storage створена разом із data.json.")


def run_servers():
    setup_storage()
    threading.Thread(target=socket_server, daemon=True).start()
    http_server = HTTPServer(('0.0.0.0', HTTP_PORT), MyHTTPRequestHandler)
    print(f"HTTP сервер запущений на порту {HTTP_PORT}")
    http_server.serve_forever()
    

if __name__ == "__main__":
    run_servers()
