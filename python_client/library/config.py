"""
ESP32 RPC Client Configuration
"""

import logging
import sys

# Result Codes
RPC_OK = 0
RPC_ERROR_INVALID_COMMAND = 1
RPC_ERROR_INVALID_PARAMS = 2
RPC_ERROR_TIMEOUT = 3
RPC_ERROR_EXECUTION = 4
RPC_ERROR_NOT_SUPPORTED = 5

# Communication Mode
COMM_USB = 0
COMM_WIFI = 1

# Debug Levels
DEBUG_NONE = 0
DEBUG_ERROR = 1
DEBUG_WARNING = 2
DEBUG_INFO = 3
DEBUG_VERBOSE = 4

# Default configuration
CONFIG = {
    'comm_mode': COMM_USB,
    'usb_port': '/dev/ttyUSB0',  # Linux/Mac: '/dev/ttyUSB0' or '/dev/ttyACM0', Windows: 'COM3'
    'usb_baudrate': 115200,
    'wifi_host': '192.168.1.100',
    'wifi_port': 5000,
    'timeout': 2.0,
    'debug': True,
    'debug_level': DEBUG_NONE,  # 0=None, 1=Error, 2=Warning, 3=Info, 4=Verbose
    'log_to_file': False,
    'log_file': 'rpc_client.log',
}

# Result code messages
RESULT_MESSAGES = {
    RPC_OK: "OK",
    RPC_ERROR_INVALID_COMMAND: "Invalid command",
    RPC_ERROR_INVALID_PARAMS: "Invalid parameters",
    RPC_ERROR_TIMEOUT: "Timeout",
    RPC_ERROR_EXECUTION: "Execution error",
    RPC_ERROR_NOT_SUPPORTED: "Not supported",
}

def get_result_message(code):
    """Get result message for result code"""
    return RESULT_MESSAGES.get(code, f"Unknown error code: {code}")

def setup_logging(debug_level=DEBUG_NONE, log_to_file=False, log_file='rpc_client.log'):
    """
    Setup logging configuration
    
    Args:
        debug_level: 0=None, 1=Error, 2=Warning, 3=Info, 4=Verbose/Debug
        log_to_file: Enable logging to file
        log_file: Log file path
    """
    # Map debug level to logging level
    level_map = {
        DEBUG_NONE: logging.CRITICAL,
        DEBUG_ERROR: logging.ERROR,
        DEBUG_WARNING: logging.WARNING,
        DEBUG_INFO: logging.INFO,
        DEBUG_VERBOSE: logging.DEBUG,
    }
    
    log_level = level_map.get(debug_level, logging.WARNING)
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    handlers = []
    
    # Console handler
    if debug_level > DEBUG_NONE:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(logging.Formatter(log_format, date_format))
        handlers.append(console_handler)
    
    # File handler
    if log_to_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(log_format, date_format))
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        handlers=handlers,
        force=True
    )
    
    # Update CONFIG
    CONFIG['debug_level'] = debug_level
    CONFIG['debug'] = debug_level > DEBUG_NONE
    CONFIG['log_to_file'] = log_to_file
    CONFIG['log_file'] = log_file
