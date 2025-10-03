"""
Configuration module for the ESP32 control system.
Contains all global configuration settings.
"""

import os
from pathlib import Path

# Root directory of the project
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Server ports
HTTP_PORT = int(os.getenv("HTTP_PORT", "5000"))
WEBSOCKET_PORT = int(os.getenv("WEBSOCKET_PORT", "8765"))
RFC2217_PORT = int(os.getenv("RFC2217_PORT", "4000"))

# Database configuration
DATABASE_PATH = str(PROJECT_ROOT / "data" / "events.db")

# Logging configuration
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")

