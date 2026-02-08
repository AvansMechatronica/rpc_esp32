# Implementation Summary - rpc_esp32

Status: complete and in active use.

## What this project delivers

An ESP32 RPC system that exposes firmware functions over USB serial or WiFi, plus a Python client library, GUI tools, and example scripts for testing and integration.

## High-level architecture

- ESP32 firmware runs an RPC server that parses JSON requests and returns JSON responses.
- Python client provides typed methods for RPC calls and handles transport over USB or WiFi.
- Optional hardware libraries (ADC, DAC, DIO, OLED, pulse, QC) are included in the firmware tree.
- GUI tools provide interactive testing and diagnostics.

## Project structure (current)

See [FILE_REFERENCE.md](FILE_REFERENCE.md) for the full file and folder index.

## Firmware components

- RPC server library: [eps32_host/lib/rpc_server](eps32_host/lib/rpc_server)
  - Server interface and implementation in [eps32_host/lib/rpc_server/include/rpc_server.h](eps32_host/lib/rpc_server/include/rpc_server.h) and [eps32_host/lib/rpc_server/src/rpc_server.cpp](eps32_host/lib/rpc_server/src/rpc_server.cpp).
  - Configuration in [eps32_host/lib/rpc_server/include/rpc_config.h](eps32_host/lib/rpc_server/include/rpc_config.h).
- Shared helpers: [eps32_host/lib/config.h](eps32_host/lib/config.h), [eps32_host/lib/bits.h](eps32_host/lib/bits.h).
- Optional device libraries:
  - ADC 3208: [eps32_host/lib/adc_lib](eps32_host/lib/adc_lib)
  - DAC 4922: [eps32_host/lib/dac_lib](eps32_host/lib/dac_lib)
  - Digital IO expander: [eps32_host/lib/dio_lib](eps32_host/lib/dio_lib)
  - OLED: [eps32_host/lib/oled_lib](eps32_host/lib/oled_lib)
  - Pulse tools: [eps32_host/lib/pulse_lib](eps32_host/lib/pulse_lib)
  - QC7366 counter: [eps32_host/lib/qc_lib](eps32_host/lib/qc_lib)
  - SPI utilities: [eps32_host/lib/spi_lib](eps32_host/lib/spi_lib)
  - USB/WiFi switch: [eps32_host/lib/usb_wifi_switch](eps32_host/lib/usb_wifi_switch)
  - WiFi config helpers: [eps32_host/lib/WifiConfigureSupport](eps32_host/lib/WifiConfigureSupport)
- Web UI assets (for WiFi config): [eps32_host/data](eps32_host/data)

## Python components

- Core client library (transport + RPC calls): [python_client/library](python_client/library)
  - RPC client: [python_client/library/rpc_client.py](python_client/library/rpc_client.py)
  - Transport layer: [python_client/library/transport.py](python_client/library/transport.py)
  - Configuration and constants: [python_client/library/config.py](python_client/library/config.py)
  - Debug helpers: [python_client/library/debug_utility.py](python_client/library/debug_utility.py)
- GUI test application: [python_client/nodeMCU_gui/nodeMCU_gui.py](python_client/nodeMCU_gui/nodeMCU_gui.py)
- Example scripts: [python_client/examples](python_client/examples)
- Debug docs: [python_client/documentation](python_client/documentation)
- Portal GUI: [python_client/portaal_robot](python_client/portaal_robot)

## RPC method coverage (overview)

The Python client exposes methods that map to firmware handlers for:

- GPIO: `pinMode`, `digitalWrite`, `digitalRead`, `analogWrite`, `analogRead`
- System: `delay`, `getMillis`, `getFreeMem`, `getChipID`
- PWM: `ledcSetup`, `ledcWrite`
- Optional modules: ADC 3208, DAC 4922, DIO, QC7366, OLED, pulse control
- Generic: `call_raw` for custom RPCs

## Communication protocol

Protocol details and examples are documented in [TECHNICAL_REFERENCE.md](TECHNICAL_REFERENCE.md).

## How to extend

Add a new RPC method by editing:

1) Firmware interface and implementation in the RPC server library.
2) Dispatcher registration in the RPC server implementation.
3) A Python wrapper in [python_client/library/rpc_client.py](python_client/library/rpc_client.py).

## Where to look next

- Entry points: [eps32_host/src/main.cpp](eps32_host/src/main.cpp) and [python_client/library/rpc_client.py](python_client/library/rpc_client.py)
- Protocol details: [TECHNICAL_REFERENCE.md](TECHNICAL_REFERENCE.md)
- Quick start: [QUICKSTART.md](QUICKSTART.md)
- File index: [FILE_REFERENCE.md](FILE_REFERENCE.md)
