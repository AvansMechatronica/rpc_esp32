# ESP32 RPC Debug - Quick Reference

## Quick Start

```bash
# Basic debug output
python example_usage.py --debug 3

# Full verbose debugging with file logging
python example_usage.py --debug 4 --log-file

# Run comprehensive debug tests
python debug_utility.py --debug 4
```

## Debug Levels

| Level | Name    | Use                  |
|-------|---------|----------------------|
| 0     | None    | Production           |
| 1     | Error   | Errors only          |
| 2     | Warning | Errors + Warnings    |
| 3     | Info    | + Info messages      |
| 4     | Verbose | Everything (debug)   |

## Command Options

### example_usage.py
```bash
-d, --debug {0,1,2,3,4}    # Set debug level
-l, --log-file             # Log to rpc_client.log
-p, --port PORT            # Serial port
```

### advanced_example.py
```bash
-d, --debug {0,1,2,3,4}    # Set debug level
-l, --log-file             # Log to rpc_client.log
-i, --iterations N         # Number of readings
--interval SECONDS         # Delay between readings
```

### debug_utility.py
```bash
# Basic options
-d, --debug {0,1,2,3,4}    # Set debug level (default: 3)
-l, --log-file             # Log to rpc_client.log
-m, --mode {usb,wifi}      # Communication mode

# Connection options
-p, --port PORT            # USB serial port
--host HOST                # WiFi host address
--wifi-port PORT           # WiFi port number

# Test selection
-t, --test TEST            # all, connection, system, gpio, 
                           # analog, speed, interactive

# Pin configuration
--gpio-pin PIN             # GPIO pin for testing (default: 13)
--adc-pin PIN              # ADC pin for testing (default: 36)
```

## Common Use Cases

### Troubleshoot Connection
```bash
python debug_utility.py --test connection --debug 4
```

### Test GPIO Operations
```bash
python debug_utility.py --test gpio --gpio-pin 2 --debug 3
```

### Measure Communication Speed
```bash
python debug_utility.py --test speed --debug 3
```

### Interactive Testing
```bash
python debug_utility.py --test interactive
# Enter: {"method": "millis", "params": {}}
```

### Test with Different Port
```bash
python example_usage.py --port /dev/ttyACM0 --debug 3
```

### Full Diagnostic with Logging
```bash
python debug_utility.py --debug 4 --log-file
cat rpc_client.log
```

## Programmatic Use

```python
from config import setup_logging, DEBUG_VERBOSE
from rpc_client import RPCClient

# Enable logging
setup_logging(debug_level=DEBUG_VERBOSE, log_to_file=True)

# Use client normally
client = RPCClient()
client.connect()
# All operations are now logged
```

## What Gets Logged

| Component   | Info Logged                                    |
|-------------|------------------------------------------------|
| Transport   | Connection, send/recv data, timeouts, errors   |
| RPC Client  | Commands, parameters, responses, parsing       |
| Examples    | Script flow, test results, exceptions          |


## [2026-01-24] Nieuw: USB verbonden, maar pinMode(2, 1) geeft geen response

- Symptoom: USB verbinding is OK, maar pinMode(2, 1) geeft "Code: 3, No response from device".
- Zie ESP32_BUG_FIX.md voor uitgebreide stappen en firmware/client checks.

## Tips

- Start with `--debug 3` for normal troubleshooting
- Use `--debug 4` only when you need full details
- Always use `--log-file` when reporting issues
- Interactive mode is great for testing custom commands
- Check log file for full request/response details

## Example Debug Session

```bash
# Terminal 1: Run with logging
python debug_utility.py --debug 4 --log-file --test all

# Terminal 2: Watch log in real-time
tail -f rpc_client.log
```

## Files Created

- `rpc_client.log` - Log file (when --log-file is used)
- `__pycache__/` - Python bytecode cache

## Documentation

- `DEBUG_GUIDE.md` - Complete debug documentation
- `DEBUG_SUMMARY.md` - Implementation summary
- `QUICKREF_DEBUG.md` - This quick reference
