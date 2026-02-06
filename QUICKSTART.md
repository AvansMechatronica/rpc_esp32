# Quick Start Guide - ESP32 RPC System

## Projectstructuur

```
rpc_esp32/
├── eps32_host/                  # ESP32 Firmware
│   ├── platformio.ini          # Build configuration
│   ├── src/main.cpp            # Server entry point
│   ├── include/                # Headers
│   └── lib/                    # Libraries
│       ├── rpc_server/         # RPC server implementation
│       ├── adc_lib/            # ADC 3208 support
│       ├── dac_lib/            # DAC 4922 support
│       ├── dio_lib/            # DIO expander support
│       ├── oled_lib/           # OLED support
│       ├── pulse_lib/          # Pulse library
│       ├── qc_lib/             # QC7366 counter support
│       ├── spi_lib/            # SPI utilities
│       └── WifiConfigureSupport/ # WiFi config helpers
│
├── python_client/              # Python Client
│   ├── library/                # Core client library
│   │   ├── rpc_client.py       # Main RPC client class
│   │   ├── transport.py        # USB/WiFi transport layer
│   │   └── config.py           # Configuration & result codes
│   ├── gui_test/               # GUI test application
│   ├── examples/               # Example scripts
│   ├── documentation/          # Debug docs
│   ├── portaal_robot/          # Portal GUI app
│   ├── __init__.py             # Package init
│   └── requirements.txt        # Python dependencies
│
├── README.md                   # Full documentation
└── QUICKSTART.md              # This file
```

## Installation (3 Schritte)

### 1. ESP32 Firmware Uploaden
```bash
cd eps32_host
pio run -e esp32doit-devkit-v1 -t upload
pio run -e esp32doit-devkit-v1 -t monitor  # Controleer output
```

### 2. Python Dependencies
```bash
cd python_client
pip install -r requirements.txt
```

### 3. Verbinding Configureren
Bewerk `python_client/config.py`:
```python
CONFIG = {
    'comm_mode': COMM_USB,           # 0=USB, 1=WiFi
    'usb_port': '/dev/ttyUSB0',      # Aanpassen voor je systeem
    'usb_baudrate': 115200,
}
```

## Snel Testen

### GUI Test (Aanbevolen)
```bash
cd python_client
python gui_test.py
```
- Klik "Connect"
- Test GPIO, System, PWM functies
- Zie responses in output

### Via Python Script
```bash
cd python_client
python example_usage.py
```

### Advanced Monitoring
```bash
cd python_client
python advanced_example.py
```

## Basis Voorbeelden

### Eenvoudige GPIO
```python
from rpc_client import RPCClient
from config import COMM_USB, RPC_OK

client = RPCClient(comm_mode=COMM_USB)
client.connect()

# Pin 13 als OUTPUT
result, msg = client.pinMode(13, 1)

# HIGH schrijven
result, msg = client.digitalWrite(13, 1)

# Lezen
result, msg, value = client.digitalRead(13)

client.disconnect()
```

### Analog Lezen
```python
# ADC pin lezen
result, msg, value = client.analogRead(36)  # 0-4095
print(f"ADC: {value}")
```

### Systeem Info
```python
# Milliseconds
result, msg, ms = client.getMillis()

# Vrij geheugen
result, msg, mem = client.getFreeMem()

# Chip ID
result, msg, id = client.getChipID()
```

### PWM/LED Dimmen
```python
# Setup PWM: channel 0, 5kHz, 8-bit (0-255)
client.ledcSetup(0, 5000, 8)

# Helderheid instellen
for brightness in [0, 64, 128, 192, 255]:
    client.ledcWrite(0, brightness)
```

### Optionele Libraries (ADC 3208, DIO, QC, OLED)
```python
# ADC 3208
result, msg, raw = client.adcReadRaw(0, averageCount=4)
result, msg, voltage = client.adcReadVoltage(0, averageCount=4)
result, msg, pressed = client.isButtonPressed(0)

# DIO
result, msg, value = client.dioGetInput()
result, msg, bit_set = client.dioIsBitSet(0)
result, msg = client.dioSetOutput(0)
result, msg = client.dioSetBit(0)
result, msg = client.dioClearBit(0)
result, msg = client.dioToggleBit(0)

# QC7366 counter
result, msg = client.qcEnableCounter(0)
result, msg, count = client.qcReadCountRegister(0)
result, msg = client.qcClearCountRegister(0)
result, msg = client.qcDisableCounter(0)

# OLED
result, msg = client.oledClear()
result, msg = client.oledWriteLine(0, "Hello", 0)
```

## Nieuwe Functies Toevoegen

### 3 Stappen om een nieuwe RPC function toe te voegen:

**1. Header (include/rpc_server.h)**
```cpp
int rpc_myNewFunction(JsonObject params);
```

**2. Implementatie (lib/rpc_server.cpp)**
```cpp
int RpcServer::rpc_myNewFunction(JsonObject params) {
  if (!params.containsKey("value")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  int val = params["value"];
  // ... do something ...
  return RPC_OK;
}

// In execute_command():
} else if (strcmp(method, "myNewFunction") == 0) {
  return rpc_myNewFunction(params);
```

**3. Python Client (rpc_client.py)**
```python
def myNewFunction(self, value: int) -> Tuple[int, str]:
    """My function description"""
    result, msg, _ = self._send_command("myNewFunction", {"value": value})
    return result, msg
```


## [2026-01-24] Nieuw: USB verbonden, maar pinMode(2, 1) geeft geen response

- Symptoom: USB verbinding is OK, maar pinMode(2, 1) geeft "Code: 3, No response from device".
- Zie ESP32_BUG_FIX.md voor uitgebreide stappen en firmware/client checks.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| USB verbinding faalt | Controleer poort: `ls /dev/tty*` |
| "No response" error | Zet `CONFIG['debug'] = True` |
| WiFi verbinding faalt | Controleer SSID in `config.h` |
| Permission denied | `sudo usermod -a -G dialout $USER` |

## Communicatie Protocol

**Request (USB/WiFi):**
```json
{"method":"digitalWrite","params":{"pin":13,"value":1}}
```

**Response:**
```json
{"result":0,"message":"OK","data":{}}
```

**Result Codes:**
- 0: RPC_OK
- 1: RPC_ERROR_INVALID_COMMAND
- 2: RPC_ERROR_INVALID_PARAMS
- 3: RPC_ERROR_TIMEOUT
- 4: RPC_ERROR_EXECUTION
- 5: RPC_ERROR_NOT_SUPPORTED

## Sterke Punten van dit Systeem

✅ **Uitbreidbaar**: Makkelijk nieuwe functies toevoegen  
✅ **Dual-mode**: USB en WiFi ondersteuning  
✅ **Result codes**: Alle operations geven feedback  
✅ **Type-safe**: Python type hints  
✅ **GUI + CLI**: Test tools inbegrepen  
✅ **Well-documented**: Voorbeelden en docs  
✅ **JSON protocol**: Duidelijk en debug-friendly  

## Volgende Stappen

1. **Test alle GPIO pins** met de GUI test app
2. **Voeg I2C/SPI** handlers toe naar behoefte
3. **Maak custom sensoren** via RPC functies
4. **Deploy WiFi** als hoofdcommunicatie kanaal

---
Veel plezier met je ESP32 RPC systeem! 🚀
