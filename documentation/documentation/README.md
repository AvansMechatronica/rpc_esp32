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
Edit <project_dir>/python_client/library/config.py and set your transport:

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

For boot-time mode selection and WiFi configure mode, see <project_dir>/QUICKSTART.md.

## Quick Start / Snel Starten

See <project_dir>/QUICKSTART.md for step-by-step setup and example usage.

## GUI Test App / GUI Test App
```bash
python python_client/nodeMCU_gui/nodeMCU_gui.py
```

## API Quick Reference / API Sneloverzicht

See <project_dir>/TECHNICAL_REFERENCE.md for the API quick reference.

## Project Structure / Projectstructuur

See <project_dir>/FILE_REFERENCE.md for the full file and folder index.

## Troubleshooting / Problemen

See <project_dir>/QUICKSTART.md for troubleshooting and common fixes.

## More Docs / Meer docs
- <project_dir>/QUICKSTART.md

## License / Licentie
[License CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
