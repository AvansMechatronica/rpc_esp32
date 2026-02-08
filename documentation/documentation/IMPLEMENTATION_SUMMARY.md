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

See <project_dir>/FILE_REFERENCE.md for the full file and folder index.

## Firmware components

- RPC server library: <project_dir>/eps32_host/lib/rpc_server
  - Server interface and implementation in <project_dir>/eps32_host/lib/rpc_server/include/rpc_server.h and <project_dir>/eps32_host/lib/rpc_server/src/rpc_server.cpp.
  - Configuration in <project_dir>/eps32_host/lib/rpc_server/include/rpc_config.h.
- Shared helpers: <project_dir>/eps32_host/lib/config.h, <project_dir>/eps32_host/lib/bits.h.
- Optional device libraries:
  - ADC 3208: <project_dir>/eps32_host/lib/adc_lib
  - DAC 4922: <project_dir>/eps32_host/lib/dac_lib
  - Digital IO expander: <project_dir>/eps32_host/lib/dio_lib
  - OLED: <project_dir>/eps32_host/lib/oled_lib
  - Pulse tools: <project_dir>/eps32_host/lib/pulse_lib
  - QC7366 counter: <project_dir>/eps32_host/lib/qc_lib
  - SPI utilities: <project_dir>/eps32_host/lib/spi_lib
  - USB/WiFi switch: <project_dir>/eps32_host/lib/usb_wifi_switch
  - WiFi config helpers: <project_dir>/eps32_host/lib/WifiConfigureSupport
- Web UI assets (for WiFi config): <project_dir>/eps32_host/data

## Python components

- Core client library (transport + RPC calls): <project_dir>/python_client/library
  - RPC client: <project_dir>/python_client/library/rpc_client.py
  - Transport layer: <project_dir>/python_client/library/transport.py
  - Configuration and constants: <project_dir>/python_client/library/config.py
  - Debug helpers: <project_dir>/python_client/library/debug_utility.py
- GUI test application: <project_dir>/python_client/nodeMCU_gui/nodeMCU_gui.py
- Example scripts: <project_dir>/python_client/examples
- Debug docs: <project_dir>/python_client/documentation
- Portal GUI: <project_dir>/python_client/portaal_robot

## RPC method coverage (overview)

The Python client exposes methods that map to firmware handlers for:

- GPIO: `pinMode`, `digitalWrite`, `digitalRead`, `analogWrite`, `analogRead`
- System: `delay`, `getMillis`, `getFreeMem`, `getChipID`
- PWM: `ledcSetup`, `ledcWrite`
- Optional modules: ADC 3208, DAC 4922, DIO, QC7366, OLED, pulse control
- Generic: `call_raw` for custom RPCs

## Communication protocol

Protocol details and examples are documented in <project_dir>/TECHNICAL_REFERENCE.md.

## How to extend

Add a new RPC method by editing:

1) Firmware interface and implementation in the RPC server library.
2) Dispatcher registration in the RPC server implementation.
3) A Python wrapper in <project_dir>/python_client/library/rpc_client.py.

## Where to look next

- Entry points: <project_dir>/eps32_host/src/main.cpp and <project_dir>/python_client/library/rpc_client.py
- Protocol details: <project_dir>/TECHNICAL_REFERENCE.md
- Quick start: <project_dir>/QUICKSTART.md
- File index: <project_dir>/FILE_REFERENCE.md
