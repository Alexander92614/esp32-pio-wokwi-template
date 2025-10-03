"""
WebSocket and Serial Bridge module for ESP32 control system.
Handles WebSocket connections and serial communication with the ESP32.
"""

import asyncio
import logging
import websockets
from typing import Set, Optional
import websockets
from typing import Any
from websockets.exceptions import ConnectionClosed
from asyncio import StreamReader, StreamWriter
from .db import log_event

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Estado global
class GlobalState:
    def __init__(self):
        self.websocket_clients: Set[Any] = set()
        self.serial_writer: Optional[StreamWriter] = None
        self.reconnect_delay: int = 5  # segundos
        self.is_running: bool = True

state = GlobalState()

async def broadcast_to_websockets(message: str) -> None:
    """
    Broadcast a message to all connected WebSocket clients.
    
    Args:
        message: The message to broadcast
    """
    if not state.websocket_clients:
        return
        
    dead_clients = set()
    for client in state.websocket_clients:
        try:
            await client.send(message)
        except Exception as e:
            logger.error(f"Error broadcasting to client: {e}")
            dead_clients.add(client)
            
    # Cleanup dead clients
    state.websocket_clients -= dead_clients

async def get_esp32_state() -> None:
    """Request the current state from the ESP32."""
    if state.serial_writer:
        try:
            state.serial_writer.write(b"GET_STATE\n")
            await state.serial_writer.drain()
        except Exception as e:
            logger.error(f"Error requesting ESP32 state: {e}")
            state.serial_writer = None

async def serial_bridge_task(RFC2217_PORT: int) -> None:
    """
    Maintain a bridge between the serial port and WebSocket clients.
    
    Args:
        RFC2217_PORT: The port number for the serial connection
    """
    while state.is_running:
        try:
            logger.info(f"Connecting to Wokwi Serial port (RFC2217) on port {RFC2217_PORT}...")
            reader, writer = await asyncio.open_connection('localhost', RFC2217_PORT)
            logger.info("Connected to Wokwi Serial port!")
            
            state.serial_writer = writer
            await get_esp32_state()
            
            while True:
                if data := await reader.readline():
                    message = data.decode().strip()
                    logger.info(f"Serial (ESP32) > {message}")
                    await broadcast_to_websockets(message)
                else:
                    break
                    
        except ConnectionRefusedError:
            logger.warning("Could not connect to Wokwi Serial port. Is the simulation running?")
        except Exception as e:
            logger.error(f"Serial bridge error: {e}")
        finally:
            logger.info(f"Serial bridge disconnected. Retrying in {state.reconnect_delay} seconds...")
            state.serial_writer = None
            await asyncio.sleep(state.reconnect_delay)

async def handle_ws_message(websocket: Any, message: str) -> None:
    """
    Handle incoming WebSocket messages.
    
    Args:
        websocket: The WebSocket connection
        message: The received message
    """
    logger.info(f"WS (Browser) > {message}")
    log_event(message)
    
    if not state.serial_writer:
        logger.warning("Message received but ESP32 is not connected.")
        return
        
    try:
        state.serial_writer.write(message.encode() + b'\n')
        await state.serial_writer.drain()
    except Exception as e:
        logger.error(f"Error sending message to ESP32: {e}")
        state.serial_writer = None

async def websocket_handler(websocket: Any) -> None:
    """
    Handle WebSocket connections and messages.
    
    Args:
        websocket: The WebSocket connection to handle
    """
    state.websocket_clients.add(websocket)
    client_id = id(websocket)
    logger.info(f"WebSocket client {client_id} connected. Total: {len(state.websocket_clients)}")
    
    try:
        await get_esp32_state()
        async for message in websocket:
            await handle_ws_message(websocket, message)
    except ConnectionClosed:
        logger.info(f"WebSocket client {client_id} connection closed normally")
    except Exception as e:
        logger.error(f"WebSocket client {client_id} error: {e}")
    finally:
        state.websocket_clients.remove(websocket)
        logger.info(f"WebSocket client {client_id} disconnected. Total: {len(state.websocket_clients)}")

async def start_ws_server(port: int, RFC2217_PORT: int) -> None:
    """
    Start the WebSocket server and serial bridge.
    
    Args:
        port: The port for the WebSocket server
        RFC2217_PORT: The port for the serial connection
    """
    state.is_running = True
    ws_server = await websockets.serve(websocket_handler, "0.0.0.0", port)
    logger.info(f"WebSocket server listening on ws://localhost:{port}")
    
    bridge_task = asyncio.create_task(serial_bridge_task(RFC2217_PORT))
    await asyncio.gather(ws_server.wait_closed(), bridge_task)
