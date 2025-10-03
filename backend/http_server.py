"""
HTTP Server module for the ESP32 control system.
Handles HTTP requests for event management and system control.
"""

import json
import asyncio
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from typing import Dict, Any, Optional
from urllib.parse import urlparse
from .db import (
    get_events, delete_db, init_db, log_event, update_event, delete_event
)
from .ws_serial import broadcast_to_websockets

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def _send_json_response(self, data: Any, status: int = 200) -> None:
        """Send a JSON response with the specified status code."""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self._add_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def _add_cors_headers(self) -> None:
        """Add CORS headers to allow cross-origin requests."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Max-Age', '86400')

    def _send_text_response(self, text: str, status: int = 200) -> None:
        """Send a text response with the specified status code."""
        self.send_response(status)
        self.send_header('Content-type', 'text/plain')
        self._add_cors_headers()
        self.end_headers()
        self.wfile.write(text.encode('utf-8'))

    def _handle_error(self, error: Exception, status: int = 400) -> None:
        """Handle errors in a consistent way."""
        self._send_text_response(f"Error: {str(error)}", status)

    def _read_json_body(self) -> Optional[Dict[str, Any]]:
        """Read and parse JSON body from request."""
        try:
            length = int(self.headers.get('Content-Length', 0))
            if length > 0:
                data = self.rfile.read(length)
                return json.loads(data)
        except Exception:
            return None
        return None

    async def _notify_websockets(self, action: str) -> None:
        """Notify WebSocket clients of an action."""
        try:
            await broadcast_to_websockets(action)
        except Exception as e:
            print(f"Error notifying WebSocket clients: {e}")

    def do_PUT(self) -> None:
        """Handle PUT requests for event updates."""
        if self.path.startswith('/events/update/'):
            try:
                event_id = int(self.path.split('/')[-1])
                payload = self._read_json_body()
                if payload and (new_command := payload.get('command')):
                    update_event(event_id, new_command)
                    asyncio.create_task(self._notify_websockets("update"))
                    self._send_text_response("Evento actualizado.")
                else:
                    self._send_text_response("Datos inválidos.", 400)
            except Exception as e:
                self._handle_error(e)
        else:
            self.send_error(404)

    def do_DELETE(self) -> None:
        """Handle DELETE requests for event deletion."""
        if self.path.startswith('/events/delete/'):
            try:
                event_id = int(self.path.split('/')[-1])
                delete_event(event_id)
                asyncio.create_task(self._notify_websockets("delete"))
                self._send_text_response("Evento eliminado.")
            except Exception as e:
                self._handle_error(e)
        else:
            self.send_error(404)

    def do_POST(self) -> None:
        """Handle POST requests for database and event operations."""
        handlers = {
            '/events/delete': lambda: (delete_db(), "Base de datos eliminada."),
            '/events/create': lambda: (init_db(), "Base de datos creada."),
            '/events/add': self._handle_event_add
        }
        
        if handler := handlers.get(self.path):
            try:
                if self.path == '/events/add':
                    result = handler()
                else:
                    result = handler()[1]
                self._send_text_response(result)
            except Exception as e:
                self._handle_error(e)
        else:
            self.send_error(404)

    def _handle_event_add(self) -> str:
        """Handle adding a new event."""
        payload = self._read_json_body()
        if payload and (command := payload.get('command')):
            log_event(command)
            asyncio.create_task(self._notify_websockets("add"))
            return "Evento agregado."
        raise ValueError("Datos inválidos.")

    def do_OPTIONS(self) -> None:
        """Handle OPTIONS requests for CORS preflight."""
        self.send_response(200)
        self._add_cors_headers()
        self.end_headers()

    def do_GET(self) -> None:
        """Handle GET requests for event retrieval."""
        if self.path == '/events':
            events = [
                {"Id": row[0], "Timestamp": row[1], "Command": row[2]}
                for row in get_events()
            ]
            self._send_json_response(events)
        elif self.path == '/events/leds':
            # Nueva ruta específica para eventos de LEDs
            all_events = get_events()
            led_events = [
                {"Id": row[0], "Timestamp": row[1], "Command": row[2]}
                for row in all_events
                if self._is_led_event(row[2])
            ]
            self._send_json_response(led_events)
        elif self.path == '/events/debug':
            rows = get_events()
            self._send_text_response('\n'.join(
                f"{row[0]} | {row[1]} | {row[2]}" for row in rows
            ))
            self.end_headers()
            for row in rows:
                self.wfile.write(f"{row[0]} | {row[1]} | {row[2]}\n".encode('utf-8'))
        else:
            super().do_GET()

    def _is_led_event(self, command: str) -> bool:
        """Check if a command is related to LED operations."""
        if not command:
            return False
        led_keywords = ['LED1', 'LED2', 'TOGGLE_1', 'TOGGLE_2']
        return any(keyword in command for keyword in led_keywords)

def run_http_server(port=5000):
    server_address = ('', port)
    httpd = ThreadingHTTPServer(server_address, CustomHTTPRequestHandler)
    print(f"Servidor HTTP corriendo en http://localhost:{port}")
    httpd.serve_forever()
