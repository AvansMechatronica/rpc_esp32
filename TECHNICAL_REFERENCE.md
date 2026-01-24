# Technical Reference - ESP32 RPC System

## Architectuur Overzicht

```
┌─────────────────────────────────────────────────────────────┐
│                    Python Host Machine                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐         ┌──────────────────┐           │
│  │   GUI Test      │         │  Custom Scripts  │           │
│  │   Application   │         │  & Applications  │           │
│  └────────┬────────┘         └────────┬─────────┘           │
│           │                           │                      │
│           └───────────┬───────────────┘                      │
│                       │                                      │
│           ┌───────────▼────────────┐                        │
│           │  RPCClient Library     │                        │
│           │ ┌────────────────────┐ │                        │
│           │ │  rpc_client.py     │ │                        │
│           │ │  - All RPC methods │ │                        │
│           │ └────────────────────┘ │                        │
│           │ ┌────────────────────┐ │                        │
│           │ │  transport.py      │ │                        │
│           │ │  - USB/WiFi layer  │ │                        │
│           │ └────────────────────┘ │                        │
│           └───────────┬────────────┘                        │
│                       │                                      │
│           ┌───────────▼────────────┐                        │
│           │   JSON/Serial Data     │                        │
│           │  (USB or TCP Socket)   │                        │
│           └───────────┬────────────┘                        │
│                       │                                      │
└───────────────────────┼──────────────────────────────────────┘
                        │
          ┌─────────────▼─────────────┐
          │   USB / WiFi Connection    │
          └─────────────┬─────────────┘
                        │
┌───────────────────────▼──────────────────────────────────────┐
│                      ESP32 Device                            │
├────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              RPC Server (main.cpp)                     │ │
│  │                                                        │ │
│  │  ┌──────────────────────────────────────────────────┐ │ │
│  │  │  Serial/WiFi Input Buffer                       │ │ │
│  │  │  JSON Parser (ArduinoJSON)                      │ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  │                      │                                 │ │
│  │  ┌──────────────────▼───────────────────────────────┐ │ │
│  │  │  Command Dispatcher                             │ │ │
│  │  │  (execute_command)                              │ │ │
│  │  └──────────────────┬───────────────────────────────┘ │ │
│  │                     │                                  │ │
│  │  ┌──────────────────▼───────────────────────────────┐ │ │
│  │  │  RPC Handler Methods                            │ │ │
│  │  │  ┌──────────────────────────────────────────┐   │ │ │
│  │  │  │ GPIO: pinMode, digitalWrite, digitalRead│   │ │ │
│  │  │  │ Analog: analogRead, analogWrite         │   │ │ │
│  │  │  │ System: delay, millis, getFreeMem       │   │ │ │
│  │  │  │ PWM: ledcSetup, ledcWrite               │   │ │ │
│  │  │  └──────────────────────────────────────────┘   │ │ │
│  │  └──────────────────┬───────────────────────────────┘ │ │
│  │                     │                                  │ │
│  │  ┌──────────────────▼───────────────────────────────┐ │ │
│  │  │  Arduino Framework Functions                    │ │ │
│  │  │  (ESP32 Hardware APIs)                          │ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  │                     │                                  │ │
│  │  ┌──────────────────▼───────────────────────────────┐ │ │
│  │  │  Response Builder & Serialization               │ │ │
│  │  │  (JSON Output)                                  │ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           ESP32 Hardware Resources                    │ │
│  │  ┌──────────────┬──────────────┬──────────────────┐   │ │
│  │  │ GPIO Pins    │  ADC Pins    │  PWM Channels    │   │ │
│  │  │ (0-39)       │  (36,37,etc) │  (0-15)          │   │ │
│  │  └──────────────┴──────────────┴──────────────────┘   │ │
│  └────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
```

## Communication Protocol Details

### JSON Message Format

**Request Structure:**
```json
{
  "method": "methodName",
  "params": {
    "param1": "value1",
    "param2": 123,
    "param3": true
  }
}
```

**Response Structure:**
```json
{
  "result": 0,
  "message": "OK",
  "data": {
    "key1": "value1",
    "key2": 456
  }
}
```

### Handshake & Communication Flow

```
1. Connect (USB/WiFi)
   └─> Device opens serial port / socket connection
       └─> ESP32 waits for JSON commands

2. Send Command
   Client: {"method":"pinMode","params":{"pin":13,"mode":1}}
   └─> Serialized as JSON string + newline

3. Parse on ESP32
   └─> ArduinoJSON deserializes request
   └─> Validates method exists
   └─> Validates required parameters

4. Execute Handler
   └─> Handler method called with params
   └─> Result code set (0 = success, 1-5 = error)
   └─> Optional data prepared

5. Send Response
   Server: {"result":0,"message":"OK","data":{}}
   └─> Serialized and sent back via serial/socket

6. Client Processes Response
   └─> JSON deserialized
   └─> Result code, message, data extracted
   └─> Returned to Python caller
```

## File Descriptions

### ESP32 Firmware

**`main.cpp`**
- Entry point: `setup()` and `loop()` functions
- Initializes RPC server
- Handles WiFi connection if enabled
- Implements serial communication loop

**`rpc_server.h`**
- Abstract RPC server class definition
- Method declarations for all supported RPC functions
- Private helper methods for request parsing and response building

**`rpc_server.cpp`**
- Complete implementation of all RPC handlers
- `execute_command()`: Dispatcher that routes to handler methods
- GPIO handlers: `rpc_pinMode()`, `rpc_digitalWrite()`, etc.
- System handlers: `rpc_delay()`, `rpc_getMillis()`, etc.
- PWM handlers: `rpc_ledcSetup()`, `rpc_ledcWrite()`

**`config.h`**
- Communication mode selection (USB or WiFi)
- Baud rate and port configurations
- WiFi SSID and password
- Result code definitions

### Python Client

**`rpc_client.py`**
- Main `RPCClient` class
- Public methods for each RPC function
- `_send_command()`: Low-level RPC call implementation
- Return format: `(result_code, message, data_dict)`

**`transport.py`**
- Abstract `Transport` base class
- `SerialTransport`: USB/serial implementation using PySerial
- `WiFiTransport`: TCP socket implementation
- `TransportFactory`: Creates appropriate transport instance

**`config.py`**
- Mode constants: `COMM_USB`, `COMM_WIFI`
- Result code constants: `RPC_OK`, `RPC_ERROR_*`
- Global `CONFIG` dictionary
- Result message mapping

**`gui_test.py`**
- Tkinter-based GUI application
- Organized tabs for different function categories
- Real-time output display
- Connection management UI

## RPC Method Reference

### GPIO Methods

```python
# Set pin mode (OUTPUT=1, INPUT=0, INPUT_PULLUP=2)
result, msg = client.pinMode(pin: int, mode: int)

# Write digital value (HIGH=1, LOW=0)
result, msg = client.digitalWrite(pin: int, value: int)

# Read digital value
result, msg, value = client.digitalRead(pin: int)

# Write PWM (0-255 for default 8-bit)
result, msg = client.analogWrite(pin: int, value: int)

# Read analog value (0-4095 on ESP32)
result, msg, value = client.analogRead(pin: int)
```

### System Methods

```python
# Sleep for milliseconds
result, msg = client.delay(ms: int)

# Get uptime in milliseconds
result, msg, millis = client.getMillis()

# Get free heap memory in bytes
result, msg, free_mem = client.getFreeMem()

# Get ESP32 chip ID
result, msg, chip_id = client.getChipID()
```

### PWM Methods

```python
# Setup PWM channel (channel 0-15, freq in Hz, bits 1-16)
result, msg = client.ledcSetup(channel: int, freq: int, bits: int)

# Write PWM duty cycle (0 to 2^bits - 1)
result, msg = client.ledcWrite(channel: int, duty: int)
```

### Raw Method

```python
# Call any RPC method with custom parameters
result, msg, data = client.call_raw(method: str, params: dict)
```

## Data Types

### Supported in Parameters
- **int** / **long**: All integer values
- **float**: Floating-point numbers
- **bool**: true/false
- **string**: Text values

### Return Values
- **result**: int (0-5, see result codes)
- **message**: string (human-readable status)
- **data**: dict (optional, contains method-specific data)
- **value**: int/float (extracted from data dict)

## Result Codes

| Code | Constant | Meaning |
|------|----------|---------|
| 0 | RPC_OK | Operation successful |
| 1 | RPC_ERROR_INVALID_COMMAND | Method not found |
| 2 | RPC_ERROR_INVALID_PARAMS | Missing/invalid parameters |
| 3 | RPC_ERROR_TIMEOUT | No response from device |
| 4 | RPC_ERROR_EXECUTION | Error during execution |
| 5 | RPC_ERROR_NOT_SUPPORTED | Function not supported |

## ESP32 Pin Configuration

### GPIO Pins
- GPIO 0-19, 21-23, 25-27, 32-39 (usable)
- GPIO 6-11: Flash memory (don't use)
- GPIO 20, 24: Not available

### ADC Pins (Analog Input)
- ADC1: GPIO 32-39 (8 channels)
- ADC2: GPIO 0, 2, 4, 12-15, 25-27 (10 channels)
- Note: ADC2 shares pins with WiFi, use ADC1 preferably

### PWM Channels
- 16 independent PWM channels (0-15)
- Configurable frequency and resolution

## Performance Characteristics

| Operation | Typical Time |
|-----------|--------------|
| USB Command Round-trip | 5-20ms |
| WiFi Command Round-trip | 10-50ms |
| GPIO Digital I/O | <1ms |
| ADC Read | 10-20ms |
| JSON Parsing (small message) | <2ms |

## Extending with New Functions

### Step-by-Step Process

**1. Define in Header** (`rpc_server.h`)
```cpp
private:
  int rpc_myFunction(JsonObject params);
```

**2. Implement Handler** (`rpc_server.cpp`)
```cpp
int RpcServer::rpc_myFunction(JsonObject params) {
  // Validate parameters
  if (!params.containsKey("requiredParam")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  // Execute
  int param = params["requiredParam"];
  // ... implementation ...
  
  // Return result
  return RPC_OK;  // or appropriate error code
}
```

**3. Register in Dispatcher** (in `execute_command()`)
```cpp
} else if (strcmp(method, "myFunction") == 0) {
  return rpc_myFunction(params);
}
```

**4. Add Python Wrapper** (`rpc_client.py`)
```python
def myFunction(self, param: int) -> Tuple[int, str]:
    """Description of myFunction"""
    result, msg, _ = self._send_command("myFunction", {"requiredParam": param})
    return result, msg
```

**5. Test with GUI or Script**
```python
result, msg = client.myFunction(42)
assert result == RPC_OK
print(f"Result: {msg}")
```

## Debugging

### Enable Debug Output

**Python Client:**
```python
from config import CONFIG
CONFIG['debug'] = True  # See all send/receive

client = RPCClient()
client.connect()
# All messages will be printed
```

**ESP32 Firmware:**
- Monitor serial output: `pio run -e esp32doit-devkit-v1 -t monitor`
- Check device connection with `Serial.println()` calls


### [2026-01-24] Nieuw: USB verbonden, maar pinMode(2, 1) geeft geen response

- Symptoom: USB verbinding is OK, maar pinMode(2, 1) geeft "Code: 3, No response from device".
- Zie ESP32_BUG_FIX.md voor uitgebreide stappen en firmware/client checks.

### Common Issues

1. **USB Port Permission Denied**
   ```bash
   sudo usermod -a -G dialout $USER
   # Restart shell
   ```

2. **Module Not Found Errors**
   ```bash
   pip install -r requirements.txt
   # Or individual: pip install pyserial
   ```

3. **Connection Timeout**
   - Check baud rate matches (115200)
   - Try different USB cable
   - Check device is powered

4. **Invalid JSON Responses**
   - Serial garbage: check baud rate
   - Partial messages: check buffer size
   - Enable debug mode to inspect

## Performance Tuning

### Reduce Latency
- Use USB instead of WiFi for low-latency
- Batch multiple commands in sequence
- Use PWM instead of repeated GPIO writes

### Reduce Power
- Use delay() to avoid busy-waiting
- Disable WiFi when using USB only
- Set appropriate PWM frequencies

### Increase Reliability
- Always check return codes
- Implement timeout handling
- Test on target hardware

---

For more details, see README.md and QUICKSTART.md
