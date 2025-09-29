import json
import asyncio
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from .db import get_events, delete_db, init_db, log_event, update_event, delete_event
from .ws_serial import broadcast_to_websockets

# Create an event loop for async operations
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)
        
    def do_PUT(self):
        if self.path.startswith('/events/update/'):
            event_id = self.path.split('/')[-1]
            length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(length)
            import json
            try:
                payload = json.loads(data)
                new_command = payload.get('command')
                if new_command:
                    update_event(event_id, new_command)
                    # Notificar por WebSocket
                    loop.run_until_complete(broadcast_to_websockets("update"))
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write("Evento actualizado.".encode('utf-8'))
                    return
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(f"Error: {e}".encode('utf-8'))
            self.send_response(400)
            self.end_headers()
            self.wfile.write("Datos inválidos.".encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    def do_DELETE(self):
        if self.path.startswith('/events/delete/'):
            event_id = self.path.split('/')[-1]
            try:
                delete_event(event_id)
                # Notificar por WebSocket
                loop.run_until_complete(broadcast_to_websockets("delete"))
                self.send_response(200)
                self.end_headers()
                self.wfile.write("Evento eliminado.".encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(f"Error: {e}".encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    def do_POST(self):
        if self.path == '/events/delete':
            delete_db()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Base de datos eliminada.")
        elif self.path == '/events/create':
            init_db()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Base de datos creada.")
        elif self.path == '/events/add':
            length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(length)
            import json
            try:
                payload = json.loads(data)
                command = payload.get('command')
                if command:
                    log_event(command)
                    # Notificar por WebSocket
                    loop.run_until_complete(broadcast_to_websockets("add"))
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"Evento agregado.")
                    return
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(f"Error: {e}".encode('utf-8'))
            self.send_response(400)
            self.end_headers()
            self.wfile.write("Datos inválidos.".encode('utf-8'))
    def do_GET(self):
        if self.path == '/events':
            events = [
                {"Id": row[0], "Timestamp": row[1], "Command": row[2]}
                for row in get_events()
            ]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(events).encode('utf-8'))
        elif self.path == '/events/debug':
            rows = get_events()
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            for row in rows:
                self.wfile.write(f"{row[0]} | {row[1]} | {row[2]}\n".encode('utf-8'))
        else:
            super().do_GET()

def run_http_server(port=5000):
    server_address = ('', port)
    httpd = ThreadingHTTPServer(server_address, CustomHTTPRequestHandler)
    print(f"Servidor HTTP corriendo en http://localhost:{port}")
    httpd.serve_forever()
