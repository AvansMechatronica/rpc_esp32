# ESP32 RPC Host/Client Application

Een volledig uitbreidbaar Remote Procedure Call (RPC) systeem voor ESP32, waarmee alle Arduino-functies van je ESP32 via Python kunnen worden aangeroepen.

## Architectuur

```
esp32_host/          - ESP32 firmware (C++ met Arduino)
├── src/main.cpp     - RPC server entry point
├── include/         - Header files
│   ├── rpc_server.h - RPC server implementatie
│   └── config.h     - Configuratie constanten
└── lib/             - Implementatie bestanden

python_client/       - Python client bibliotheek
├── rpc_client.py    - RPC client klasse
├── transport.py     - USB/WiFi transport layer
├── config.py        - Configuratie en result codes
├── gui_test.py      - GUI testprogramma
└── requirements.txt - Python dependencies
```

## Features

### ESP32 Firmware
- **Dual-mode communicatie**: USB (serial) en WiFi TCP socket
- **JSON-gebaseerd RPC protocol** voor duidelijke communicatie
- **Result codes** voor elke operatie
- **Uitbreidbaar systeem**: Makkelijk nieuwe functies toevoegen

### Ondersteunde Arduino Functions
- **GPIO**: `pinMode()`, `digitalWrite()`, `digitalRead()`
- **Analog**: `analogWrite()`, `analogRead()`
- **PWM**: `ledcSetup()`, `ledcWrite()`
- **System**: `delay()`, `millis()`, free memory, chip ID

### Python Client Library
- **Transport abstraction**: Eenvoudig switch tussen USB en WiFi
- **Type-safe API**: Alle functies retourneren (result_code, message, data)
- **Async-ready**: Ontworpen voor toekomstige async extensies

### GUI Test Program
- **Volledig georganiseerde interface** met tabbladen per categorie
- **Real-time output**: Zie alle RPC calls en responses
- **Connection management**: Verbinding beheren vanuit GUI
- **Raw command support**: Test custom RPC functies

## Installatie

### ESP32 Firmware
1. PlatformIO gebruiken:
```bash
cd eps32_host
pio run -e esp32doit-devkit-v1  # Build
pio run -e esp32doit-devkit-v1 -t upload  # Upload
pio run -e esp32doit-devkit-v1 -t monitor  # Monitor
```

### Python Client
1. Installeer dependencies:
```bash
cd python_client
pip install -r requirements.txt
```

2. Configureer verbinding in `config.py`:
```python
CONFIG = {
    'comm_mode': COMM_USB,  # COMM_WIFI voor WiFi
    'usb_port': '/dev/ttyUSB0',  # Pas aan voor je systeem
    'usb_baudrate': 115200,
    'wifi_host': '192.168.1.100',
    'wifi_port': 5000,
}
```

## Gebruik

### Via GUI Test Program
```bash
python gui_test.py
```

### Via Python Script
```python
from rpc_client import RPCClient
from config import COMM_USB

# Maak client aan
client = RPCClient(comm_mode=COMM_USB)

# Verbind
success, message = client.connect()
if success:
    # Zet GPIO pin 13 naar OUTPUT
    result, msg = client.pinMode(13, 1)
    if result == 0:  # RPC_OK
        print("Succes!")
    
    # Schrijf HIGH naar pin
    result, msg = client.digitalWrite(13, 1)
    
    # Lees analoge waarde
    result, msg, value = client.analogRead(36)
    print(f"Analog value: {value}")
    
    client.disconnect()
```

## RPC Protocol

### Request Format
```json
{
  "method": "digitalWrite",
  "params": {
    "pin": 13,
    "value": 1
  }
}
```

### Response Format
```json
{
  "result": 0,
  "message": "OK",
  "data": {
    "value": 123
  }
}
```

### Result Codes
- `0`: RPC_OK - Succes
- `1`: RPC_ERROR_INVALID_COMMAND - Onbekende command
- `2`: RPC_ERROR_INVALID_PARAMS - Ontbrekende/ongeldige parameters
- `3`: RPC_ERROR_TIMEOUT - Geen respons
- `4`: RPC_ERROR_EXECUTION - Uitvoeringsfout
- `5`: RPC_ERROR_NOT_SUPPORTED - Niet ondersteund

## Nieuwe RPC Functies Toevoegen

### 1. In ESP32 Firmware (rpc_server.h)
```cpp
// Voeg method declaration toe
int rpc_myFunction(JsonObject params);
```

### 2. In rpc_server.cpp
```cpp
// Implementatie
int RpcServer::rpc_myFunction(JsonObject params) {
  if (!params.containsKey("myParam")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  int value = params["myParam"];
  // ... doe iets ...
  
  return RPC_OK;
}

// Voeg toe aan execute_command
} else if (strcmp(method, "myFunction") == 0) {
  return rpc_myFunction(params);
}
```

### 3. In Python Client (rpc_client.py)
```python
def myFunction(self, myParam: int) -> Tuple[int, str]:
    """My function description"""
    result, msg, _ = self._send_command("myFunction", {"myParam": myParam})
    return result, msg
```

## USB/WiFi Configuratie

### USB Mode (Default)
- Geen extra configuratie nodig
- Baud rate: 115200
- Cross-platform: Linux, macOS, Windows

### WiFi Mode
1. Wijzig in `config.h` (ESP32):
```cpp
#define CONFIG_COMM_MODE COMM_WIFI
#define CONFIG_WIFI_SSID "YOUR_SSID"
#define CONFIG_WIFI_PASSWORD "YOUR_PASSWORD"
```

2. Upload firmware

3. Wijzig in Python `config.py`:
```python
CONFIG = {
    'comm_mode': COMM_WIFI,
    'wifi_host': 'ESP32_IP',
    'wifi_port': 5000,
}
```

## Troubleshooting

### USB Verbinding Mislukt
- Controleer USB-poort: `ls /dev/tty*` (Linux/Mac)
- Installeer CH340 driver voor sommige boards
- Test met: `pio run -e esp32doit-devkit-v1 -t monitor`

### WiFi Verbinding Mislukt
- Controleer SSID en wachtwoord in `config.h`
- Zet debug aan: `CONFIG['debug'] = True`
- Controleer IP-adres in serial monitor

### "Not connected" Error
- Zorg dat `client.connect()` met True terugkeert
- Check debug output voor foutmeldingen

## Voorbeelden

Zie `python_client/gui_test.py` voor volledige voorbeelden van:
- GPIO operations
- System monitoring
- PWM control
- Raw RPC calls

## Licentie

MIT
