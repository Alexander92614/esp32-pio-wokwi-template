import asyncio
import websockets
import threading
from .db import log_event

websocket_clients = set()
serial_writer = None

async def broadcast_to_websockets(message):
    if websocket_clients:
        await asyncio.gather(*[client.send(message) for client in websocket_clients])

async def serial_bridge_task(RFC2217_PORT):
    global serial_writer
    while True:
        try:
            print(f"Conectando al puerto Serie de Wokwi (RFC2217) en el puerto {RFC2217_PORT}...")
            reader, writer = await asyncio.open_connection('localhost', RFC2217_PORT)
            print("¡Conectado al puerto Serie de Wokwi!")
            serial_writer = writer
            writer.write(b"GET_STATE\n")
            await writer.drain()
            while True:
                data = await reader.readline()
                if not data:
                    break
                message = data.decode().strip()
                print(f"Serial (ESP32) > {message}")
                await broadcast_to_websockets(message)
        except ConnectionRefusedError:
            print("No se pudo conectar al puerto Serie de Wokwi. ¿Está la simulación corriendo?")
        except Exception as e:
            print(f"Error en el puente Serie: {e}")
        finally:
            print("Puente Serie desconectado. Reintentando en 5 segundos...")
            serial_writer = None
            await asyncio.sleep(5)

async def websocket_handler(websocket):
    websocket_clients.add(websocket)
    print(f"Cliente WebSocket conectado. Total: {len(websocket_clients)}")
    try:
        if serial_writer:
            serial_writer.write(b"GET_STATE\n")
            await serial_writer.drain()
        async for message in websocket:
            print(f"WS (Browser) > {message}")
            log_event(message)
            if serial_writer:
                serial_writer.write(message.encode() + b'\n')
                await serial_writer.drain()
            else:
                print("Advertencia: Mensaje de WS recibido, pero el ESP32 no está conectado.")
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        websocket_clients.remove(websocket)
        print(f"Cliente WebSocket desconectado. Total: {len(websocket_clients)}")

async def start_ws_server(port, RFC2217_PORT):
    import websockets
    ws_server = await websockets.serve(websocket_handler, "0.0.0.0", port)
    print(f"Servidor WebSocket escuchando en ws://localhost:{port}")
    bridge_task = asyncio.create_task(serial_bridge_task(RFC2217_PORT))
    await asyncio.gather(ws_server.wait_closed(), bridge_task)
