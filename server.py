import asyncio
import threading
import os
from pathlib import Path
from backend.db import init_db
from backend.http_server import run_http_server
from backend.ws_serial import start_ws_server

# Configuración de puertos
HTTP_PORT = 5000
WEBSOCKET_PORT = 8765
RFC2217_PORT = 4000

# Asegurarse de que el directorio data existe
data_dir = Path(__file__).parent / 'data'
data_dir.mkdir(exist_ok=True)

def main():
    # Inicializar la base de datos
    init_db()
    print(f"Servidor HTTP corriendo en http://localhost:{HTTP_PORT}")
    
    # Iniciar el servidor HTTP en un hilo separado
    http_thread = threading.Thread(target=run_http_server, args=(HTTP_PORT,), daemon=True)
    http_thread.start()
    
    try:
        # Iniciar el servidor WebSocket y la conexión serial
        print(f"Servidor WebSocket escuchando en ws://localhost:{WEBSOCKET_PORT}")
        asyncio.run(start_ws_server(WEBSOCKET_PORT, RFC2217_PORT))
    except KeyboardInterrupt:
        print("\nServidor detenido.")

if __name__ == "__main__":
    main()