"""
ESP32 RPC Client Library

A complete RPC (Remote Procedure Call) system for ESP32
"""

from .rpc_client import RPCClient
from .transport import Transport, SerialTransport, WiFiTransport, TransportFactory
from .config import (
    COMM_USB, COMM_WIFI,
    RPC_OK, RPC_ERROR_INVALID_COMMAND, RPC_ERROR_INVALID_PARAMS,
    RPC_ERROR_TIMEOUT, RPC_ERROR_EXECUTION, RPC_ERROR_NOT_SUPPORTED,
    get_result_message, CONFIG
)

__version__ = "1.0.0"
__author__ = "ESP32 RPC Developer"

__all__ = [
    'RPCClient',
    'Transport',
    'SerialTransport',
    'WiFiTransport',
    'TransportFactory',
    'COMM_USB',
    'COMM_WIFI',
    'RPC_OK',
    'RPC_ERROR_INVALID_COMMAND',
    'RPC_ERROR_INVALID_PARAMS',
    'RPC_ERROR_TIMEOUT',
    'RPC_ERROR_EXECUTION',
    'RPC_ERROR_NOT_SUPPORTED',
    'get_result_message',
    'CONFIG',
]
