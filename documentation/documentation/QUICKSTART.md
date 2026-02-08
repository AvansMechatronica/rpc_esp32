# Quick Start Guide - ESP32 RPC System

## Projectstructuur

Zie [FILE_REFERENCE.md](FILE_REFERENCE.md) voor de volledige bestandsstructuur.

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


#### USB/WiFi mode kiezen tijdens boot

Je kunt de communicatie-mode ook kiezen tijdens het opstarten van de ESP32-NodeMCU:

- Houd knop 0 ingedrukt tijdens boot om de mode te selecteren.
- Laat los na boot om de geselecteerde mode te gebruiken.

#### WiFi configure mode tijdens boot

Als de ESP32 in WiFi mode staat:

- Houd knop 1 ingedrukt tijdens boot om WiFi configure mode te openen.

## Snel Testen

### GUI Test (Aanbevolen)
```bash
cd python_client/nodeMCU_gui
python nodeMCU_gui.py
```
- Klik "Connect"
- Test GPIO, System, PWM functies
- Zie responses in output

### Via Python Script
```bash
cd python_client/examples
python example_usage.py
```

### Advanced Monitoring
```bash
cd python_client/examples
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


## Troubleshooting

| Problem | Solution |
|---------|----------|
| USB verbinding faalt | Controleer poort: `ls /dev/tty*` |
| "No response" error | Zet `CONFIG['debug'] = True` |
| WiFi verbinding faalt | Controleer SSID in `config.h` |
| Permission denied | `sudo usermod -a -G dialout $USER` |

## Meer details

- Protocol, result codes en uitbreiden: [TECHNICAL_REFERENCE.md](TECHNICAL_REFERENCE.md)

---
Veel plezier met je ESP32-NodeMCU RPC systeem! 🚀
