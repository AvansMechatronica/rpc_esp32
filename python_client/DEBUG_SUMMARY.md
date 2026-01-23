# ESP32 RPC Python Client - Debug Features Summary

## Overview
Comprehensive debug functionality has been added to all Python scripts in the ESP32 RPC client library.

## Changes Made

### 1. Enhanced config.py
- Added Python `logging` module support
- Defined 5 debug levels (NONE, ERROR, WARNING, INFO, VERBOSE)
- Added `setup_logging()` function for configuring logging
- Support for console and file logging
- Configurable log format with timestamps

### 2. Updated rpc_client.py
- Added logging throughout the RPC client
- Logs all method calls, parameters, and responses
- Tracks connection state changes
- Detailed JSON request/response logging
- Error and exception tracking

### 3. Updated transport.py
- Added logging to both SerialTransport and WiFiTransport
- Logs connection attempts and results
- Tracks data transmission (send/receive)
- Logs timeout events
- Detailed error information

### 4. Enhanced example_usage.py
- Added argparse for command-line arguments
- Support for `--debug` level (0-4)
- Support for `--log-file` option
- Support for `--port` selection
- Logging of script execution flow

### 5. Enhanced advanced_example.py
- Added argparse for command-line arguments
- Support for `--debug` level (0-4)
- Support for `--log-file` option
- Configurable `--iterations` and `--interval`
- Logging throughout monitor operations

### 6. New: debug_utility.py
A comprehensive debugging tool with:
- Connection testing
- System information retrieval
- GPIO operation testing
- Analog read testing
- Communication speed benchmarking
- Interactive mode for manual testing
- Extensive command-line options
- Support for both USB and WiFi modes

### 7. New: DEBUG_GUIDE.md
Complete documentation including:
- Debug level descriptions
- Usage examples
- Command-line options
- Troubleshooting guide
- Log file format
- Best practices

## Usage Examples

### Basic Debug Output
```bash
# Info level debugging
python example_usage.py --debug 3

# Verbose debugging with file logging
python example_usage.py --debug 4 --log-file
```

### Debug Utility
```bash
# Run all tests
python debug_utility.py

# Test specific functionality
python debug_utility.py --test gpio --gpio-pin 13 --debug 4

# Interactive mode
python debug_utility.py --test interactive
```

### Programmatic Use
```python
from config import setup_logging, DEBUG_VERBOSE
from rpc_client import RPCClient

# Enable verbose logging
setup_logging(debug_level=DEBUG_VERBOSE, log_to_file=True)

# Use client as normal - all operations will be logged
client = RPCClient()
```

## Debug Levels

| Level | Name | Description | Use Case |
|-------|------|-------------|----------|
| 0 | DEBUG_NONE | No output | Production |
| 1 | DEBUG_ERROR | Errors only | Production with error tracking |
| 2 | DEBUG_WARNING | Errors + warnings | Basic troubleshooting |
| 3 | DEBUG_INFO | + informational | Development |
| 4 | DEBUG_VERBOSE | All messages | Deep debugging |

## Key Features

1. **Hierarchical Logging**: Uses Python's standard logging module
2. **Configurable Output**: Console and/or file logging
3. **Detailed Tracking**: Full request/response logging
4. **Performance Metrics**: Communication speed testing
5. **Interactive Testing**: Manual command entry mode
6. **Cross-Platform**: Works on Linux, macOS, Windows
7. **Non-Intrusive**: Zero impact when debug level = 0

## Files Modified
- `python_client/config.py` - Added logging configuration
- `python_client/rpc_client.py` - Added logging statements
- `python_client/transport.py` - Added logging statements
- `python_client/example_usage.py` - Added argparse and logging
- `python_client/advanced_example.py` - Added argparse and logging

## Files Created
- `python_client/debug_utility.py` - Comprehensive debug tool
- `python_client/DEBUG_GUIDE.md` - Complete debug documentation
- `python_client/DEBUG_SUMMARY.md` - This file

## Testing the Debug Features

```bash
# Test basic functionality with debugging
cd /home/gerard/rpc_esp32/python_client

# Run debug utility (requires ESP32 connected)
python debug_utility.py --debug 4 --log-file

# Check log file
cat rpc_client.log
```

## Benefits

1. **Faster Debugging**: Detailed logs help identify issues quickly
2. **Better Diagnostics**: See exactly what's being sent/received
3. **Performance Analysis**: Measure communication speed
4. **Production Ready**: Disable debug output for production use
5. **Comprehensive Testing**: Debug utility tests all major functions
6. **Educational**: Learn how the RPC protocol works

## Notes

- All scripts remain backward compatible
- Debug features are opt-in (disabled by default)
- No external dependencies required (uses Python standard library)
- Log files use standard format compatible with log analysis tools
