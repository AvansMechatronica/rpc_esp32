# ESP32 RPC Python Client - Debug Features

This document describes the comprehensive debugging features available in the ESP32 RPC Python client.

## Debug Levels

The client supports 5 debug levels for controlling the verbosity of logging output:

- **Level 0 (DEBUG_NONE)**: No debug output
- **Level 1 (DEBUG_ERROR)**: Only errors
- **Level 2 (DEBUG_WARNING)**: Errors and warnings
- **Level 3 (DEBUG_INFO)**: Errors, warnings, and informational messages
- **Level 4 (DEBUG_VERBOSE)**: All messages including detailed debug information

## Enabling Debug Output

### Command-Line Arguments

All example scripts support command-line arguments for debugging:

```bash
# Run with info-level debugging
python example_usage.py --debug 3

# Run with verbose debugging and log to file
python example_usage.py --debug 4 --log-file

# Run advanced example with debug level 3
python advanced_example.py -d 3 -i 10 --interval 1.0
```

### Programmatic Configuration

You can also enable debugging programmatically in your own scripts:

```python
from config import setup_logging, DEBUG_INFO, DEBUG_VERBOSE

# Setup logging with info level
setup_logging(debug_level=DEBUG_INFO)

# Setup logging with verbose level and file output
setup_logging(debug_level=DEBUG_VERBOSE, log_to_file=True, log_file='my_debug.log')
```

## Debug Utility Script

A dedicated debug utility script (`debug_utility.py`) is provided for comprehensive testing and debugging:

### Basic Usage

```bash
# Run all tests with default settings
python debug_utility.py

# Run specific test
python debug_utility.py --test connection
python debug_utility.py --test system
python debug_utility.py --test gpio
python debug_utility.py --test analog
python debug_utility.py --test speed

# Interactive mode for manual testing
python debug_utility.py --test interactive
```

### Advanced Options

```bash
# Use different serial port
python debug_utility.py -p /dev/ttyACM0

# Test with WiFi mode
python debug_utility.py --mode wifi --host 192.168.1.100 --wifi-port 5000

# Set debug level
python debug_utility.py --debug 4

# Test specific GPIO/ADC pins
python debug_utility.py --test gpio --gpio-pin 2
python debug_utility.py --test analog --adc-pin 39

# Enable file logging
python debug_utility.py --debug 4 --log-file
```

### Available Tests

1. **Connection Test**: Verifies connection to ESP32
2. **System Information Test**: Retrieves chip ID, free memory, uptime
3. **GPIO Operations Test**: Tests digital I/O operations
4. **Analog Operations Test**: Tests ADC readings
5. **Communication Speed Test**: Measures RPC round-trip time
6. **Interactive Mode**: Manual command entry for custom testing

### Interactive Mode

In interactive mode, you can send raw RPC commands:

```bash
python debug_utility.py --test interactive
```

Example commands:
```json
{"method": "millis", "params": {}}
{"method": "pinMode", "params": {"pin": 13, "mode": 1}}
{"method": "digitalWrite", "params": {"pin": 13, "value": 1}}
{"method": "analogRead", "params": {"pin": 36}}
```

Type `quit` or press Ctrl+C to exit.

## What Gets Logged

### Transport Layer (transport.py)

- Connection attempts and results
- Data transmission (with size information)
- Data reception (with size information)
- Timeouts and errors
- Transport initialization

### RPC Client Layer (rpc_client.py)

- Client initialization
- Connection/disconnection events
- Command requests (method and parameters)
- JSON request/response data
- Command results and errors
- Response parsing errors

### Example Scripts

- Script start/completion
- Argument parsing
- Test execution progress
- Errors and exceptions

## Log File Format

When file logging is enabled, logs are written in the following format:

```
2026-01-23 10:30:45 - transport - INFO - Connecting to serial port: /dev/ttyUSB0
2026-01-23 10:30:47 - transport - INFO - Successfully connected to /dev/ttyUSB0
2026-01-23 10:30:47 - rpc_client - INFO - Successfully connected to ESP32
2026-01-23 10:30:47 - rpc_client - DEBUG - _send_command called: method=millis, params={}
2026-01-23 10:30:47 - rpc_client - DEBUG - Request JSON: {"method": "millis", "params": {}}
2026-01-23 10:30:47 - transport - DEBUG - Sending data: {"method": "millis", "params": {}}
2026-01-23 10:30:47 - transport - DEBUG - Received data: {"result": 0, "message": "OK", "data": {"millis": 12345}}
2026-01-23 10:30:47 - rpc_client - DEBUG - Command successful: millis, data={'millis': 12345}
```

## Debugging Tips

### Connection Issues

Enable verbose logging to see connection attempts:
```bash
python example_usage.py --debug 4
```

Check for:
- Correct serial port
- ESP32 properly connected
- Correct baud rate (default: 115200)
- USB driver issues

### Communication Timeouts

Use the debug utility to test communication speed:
```bash
python debug_utility.py --test speed --debug 4
```

Check for:
- Slow or inconsistent response times
- ESP32 firmware responsiveness
- Serial buffer issues

### Command Failures

Enable debug logging to see full request/response data:
```bash
python example_usage.py --debug 4 --log-file
```

Check the log file for:
- Malformed JSON requests
- Invalid parameters
- ESP32 error responses
- Missing or unexpected data fields

### Custom Debugging

Create your own debug script:

```python
#!/usr/bin/env python3
import logging
from rpc_client import RPCClient
from config import setup_logging, DEBUG_VERBOSE, COMM_USB

# Enable verbose logging
setup_logging(debug_level=DEBUG_VERBOSE, log_to_file=True)

# Get logger
logger = logging.getLogger(__name__)

# Your code here
logger.info("Starting custom test")
client = RPCClient(comm_mode=COMM_USB)
# ... rest of your code
```

## Performance Considerations

- **Level 4 (Verbose)**: Can slow down high-frequency operations due to extensive logging
- **File Logging**: Adds I/O overhead, use for debugging only
- **Production Use**: Set debug level to 0 or 1 for production deployments

## Environment Variables

You can also set debug options via code before importing:

```python
# Set before importing
import sys
sys.path.insert(0, 'python_client')

from config import CONFIG
CONFIG['debug_level'] = 4
CONFIG['log_to_file'] = True

# Now import and use
from rpc_client import RPCClient
```


## [2026-01-24] Nieuw: USB verbonden, maar pinMode(2, 1) geeft geen response

- Symptoom: USB verbinding is OK, maar pinMode(2, 1) geeft "Code: 3, No response from device".
- Zie ESP32_BUG_FIX.md voor uitgebreide stappen en firmware/client checks.

## Troubleshooting Common Issues

### Issue: No debug output appears

**Solution**: Make sure debug level > 0:
```bash
python example_usage.py --debug 3
```

### Issue: Log file not created

**Solution**: Use the `--log-file` flag:
```bash
python example_usage.py --debug 3 --log-file
```

### Issue: Too much debug output

**Solution**: Lower the debug level:
```bash
python example_usage.py --debug 2  # Warnings and errors only
```

### Issue: Can't see transport layer details

**Solution**: Use verbose (level 4) debugging:
```bash
python example_usage.py --debug 4
```

## Example Debug Session

Here's a complete example of debugging a connection issue:

```bash
# Start with verbose debugging and file logging
$ python debug_utility.py --debug 4 --log-file -p /dev/ttyUSB0

Initializing RPC Client in USB mode...

============================================================
CONNECTION TEST
============================================================
2026-01-23 10:30:45 - transport - INFO - Connecting to serial port: /dev/ttyUSB0
2026-01-23 10:30:47 - transport - INFO - Successfully connected to /dev/ttyUSB0
✓ Connection successful: Connected successfully

============================================================
SYSTEM INFORMATION TEST
============================================================
2026-01-23 10:30:47 - rpc_client - DEBUG - _send_command called: method=chipID, params={}
✓ Chip ID: 0x12345678
✓ Free Memory: 245760 bytes (240.00 KB)
✓ Uptime: 12345 ms (12.35 seconds)

# Check the log file for detailed information
$ cat rpc_client.log
```

This comprehensive debug system helps you quickly identify and resolve issues with ESP32 RPC communication!
