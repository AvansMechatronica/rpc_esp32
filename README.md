# ESP32 RPC Python Client

EN: Python client and GUI for controlling an ESP32 over RPC (USB serial or WiFi). This README focuses on Python usage; the ESP32 firmware must already be flashed with the RPC server.

NL: Python client en GUI om een ESP32 via RPC aan te sturen (USB serial of WiFi). Deze README focust op Python; de ESP32 firmware met RPC server moet al geflasht zijn.

## Features / Functionaliteit
- EN: Typed Python API with clear result codes; GUI test app; optional modules (ADC 3208, DAC 4922, DIO, QC7366, OLED, pulse library).
- NL: Type-safe Python API met duidelijke result codes; GUI test app; optionele modules (ADC 3208, DAC 4922, DIO, QC7366, OLED, pulse library).

## Requirements / Vereisten
- EN: Python 3.9+; ESP32 running the RPC firmware; USB serial driver if needed.
- NL: Python 3.9+; ESP32 met RPC firmware; USB serial driver indien nodig.

## Install / Installatie
```bash
cd python_client
pip install -r requirements.txt
```

## Configure Connection / Verbinding Configureren
Edit [python_client/library/config.py](python_client/library/config.py) and set your transport:

USB example:
```python
CONFIG = {
    "comm_mode": COMM_USB,
    "usb_port": "COM3",  # Windows example
    "usb_baudrate": 115200,
}
```

WiFi example:
```python
CONFIG = {
    "comm_mode": COMM_WIFI,
    "wifi_host": "192.168.1.100",
    "wifi_port": 5000,
}
```

## Quick Start / Snel Starten
```python
from python_client.library.rpc_client import RPCClient
from python_client.library.config import COMM_USB, RPC_OK

client = RPCClient(comm_mode=COMM_USB)
ok, msg = client.connect()
if ok:
    result, msg = client.pinMode(13, 1)
    result, msg = client.digitalWrite(13, 1)
    result, msg, value = client.analogRead(36)
    if result == RPC_OK:
        print("ADC:", value)
    client.disconnect()
```

## GUI Test App / GUI Test App
```bash
python python_client/gui_test/gui_test.py
```

## API Quick Reference / API Sneloverzicht
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

EN: Optional APIs require matching firmware features enabled.
NL: Optionele APIs vereisen bijpassende firmware features.

## Project Structure / Projectstructuur
```
rpc_esp32/
├── eps32_host/                  # ESP32 firmware (RPC server)
├── python_client/               # Python client + GUI
│   ├── library/                 # Core client library
│   ├── gui_test/                # GUI tabs
│   ├── examples/                # Example scripts
│   └── documentation/           # Debug docs
├── QUICKSTART.md                # Extended quick start
└── README.md                    # This file
```

## Troubleshooting / Problemen
- EN: "Not connected" -> verify `client.connect()` and port settings in [python_client/library/config.py](python_client/library/config.py).
- EN: "No response" -> check firmware is running and USB baud rate.
- NL: "Not connected" -> controleer `client.connect()` en poort in [python_client/library/config.py](python_client/library/config.py).
- NL: "No response" -> controleer firmware en USB baudrate.

## More Docs / Meer docs
- [QUICKSTART.md](QUICKSTART.md)

## License / Licentie
MIT
