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

For the complete file index, see <project_dir>/FILE_REFERENCE.md.

Key entry points:

- <project_dir>/eps32_host/src/main.cpp - Firmware entry point and main loop.
- <project_dir>/eps32_host/lib/rpc_server/src/rpc_server.cpp - RPC request dispatch and handlers.
- <project_dir>/python_client/library/rpc_client.py - Python RPC client interface.
- <project_dir>/python_client/library/transport.py - USB/WiFi transport implementations.

Boot-time mode selection and WiFi configure mode are documented in <project_dir>/QUICKSTART.md.

## RPC Method Reference

## API Quick Reference

- GPIO: `pinMode`, `digitalWrite`, `digitalRead`
- Analog: `analogWrite`, `analogRead`
- PWM: `ledcSetup`, `ledcWrite`
- System: `delay`, `getMillis`, `getFreeMem`, `getChipID`
- Pulse: `pulseBegin`, `pulse`, `pulseAsync`, `isPulsing`, `generatePulses`, `generatePulsesAsync`, `getRemainingPulses`, `stopPulse`
- ADC 3208: `adcReadRaw`, `adcReadVoltage`, `isButtonPressed`
- DAC 4922: `dacSetVoltage`, `dacSetVoltageAll`
- DIO: `dioGetInput`, `dioIsBitSet`, `dioSetOutput`, `dioSetBit`, `dioClearBit`, `dioToggleBit`
- QC7366: `qcEnableCounter`, `qcDisableCounter`, `qcClearCountRegister`, `qcReadCountRegister`
- OLED: `oledClear`, `oledWriteLine`

Optional APIs require matching firmware features enabled.

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

For setup, troubleshooting, and debug steps, see <project_dir>/QUICKSTART.md.

---

For more details, see README.md and QUICKSTART.md
