#!/usr/bin/env python3
"""
Main server integrating WebSocket and HTTP for ESP32 control.
"""

import os
import sys
from pathlib import Path

# Configure path for imports
PROJECT_ROOT = Path(__file__).parent.absolute()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json
import asyncio
import logging
import threading
from datetime import datetime
from typing import Dict, Any
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('server.log')
    ]
)

logger = logging.getLogger(__name__)

# Import local modules after setting up Python path
from backend import (
    HTTP_PORT, WEBSOCKET_PORT, RFC2217_PORT
)
from backend.db import init_db
from backend.http_server import run_http_server
from backend.ws_serial import start_ws_server

# Import local modules after setting up configuration
from backend.db import init_db
from backend.http_server import run_http_server
from backend.ws_serial import start_ws_server

async def start_all_services() -> None:
    """Initialize and start all server services."""
    http_thread = None
    try:
        # Initialize database
        init_db()
        logger.info("Database initialized successfully")
        
        # Start HTTP server in a separate thread
        http_thread = threading.Thread(
            target=run_http_server, 
            args=(HTTP_PORT,), 
            daemon=True
        )
        http_thread.start()
        logger.info(f"HTTP server started on http://localhost:{HTTP_PORT}")
        
        # Start WebSocket server
        await start_ws_server(WEBSOCKET_PORT, RFC2217_PORT)
    except Exception as e:
        logger.error(f"Failed to start services: {e}")
        raise
    finally:
        # Clean up threads
        if http_thread:
            try:
                http_thread.join(timeout=1.0)
            except Exception as e:
                logger.error(f"Error shutting down HTTP thread: {e}")

def main() -> None:
    """Main entry point for the server."""
    try:
        # Configure asyncio event loop policy for Windows
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        # Start all services
        asyncio.run(start_all_services())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == '__main__':
    main()