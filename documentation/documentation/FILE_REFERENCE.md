# File Reference - rpc_esp32

This document is a complete, current index of files and folders in the workspace. It focuses on structure and purpose.

## Top-level documentation

- <project_dir>/README.md - Main project overview and Python client usage.
- <project_dir>/QUICKSTART.md - Quick start steps and example workflows.
- <project_dir>/TECHNICAL_REFERENCE.md - Architecture and protocol details.
- <project_dir>/IMPLEMENTATION_SUMMARY.md - Build summary and feature list.
- <project_dir>/FILE_REFERENCE.md - This index.

## ESP32 firmware (eps32_host)

- <project_dir>/eps32_host/platformio.ini - PlatformIO build configuration.
- <project_dir>/eps32_host/src/main.cpp - Firmware entry point.
- <project_dir>/eps32_host/include/README - Notes for the include folder.
- <project_dir>/eps32_host/test/README - Test folder notes.

### Core firmware libraries (eps32_host/lib)

- <project_dir>/eps32_host/lib/config.h - Firmware configuration and result codes.
- <project_dir>/eps32_host/lib/bits.h - Bit utilities and helpers.
- <project_dir>/eps32_host/lib/README - Library notes.

### RPC server library (eps32_host/lib/rpc_server)

- <project_dir>/eps32_host/lib/rpc_server/library.properties - Arduino library metadata.
- <project_dir>/eps32_host/lib/rpc_server/include/rpc_config.h - RPC configuration definitions.
- <project_dir>/eps32_host/lib/rpc_server/include/rpc_server.h - RPC server interface.
- <project_dir>/eps32_host/lib/rpc_server/src/rpc_server.cpp - RPC server implementation.

### Optional hardware libraries (eps32_host/lib)

- <project_dir>/eps32_host/lib/adc_lib/adc_3208_lib.h - MCP3208 ADC interface.
- <project_dir>/eps32_host/lib/adc_lib/adc_3208_lib.cpp - MCP3208 ADC implementation.
- <project_dir>/eps32_host/lib/dac_lib/dac_4922_lib.h - MCP4922 DAC interface.
- <project_dir>/eps32_host/lib/dac_lib/dac_4922_lib.cpp - MCP4922 DAC implementation.
- <project_dir>/eps32_host/lib/dio_lib/dio_lib.h - Digital IO expander interface.
- <project_dir>/eps32_host/lib/dio_lib/dio_lib.cpp - Digital IO expander implementation.
- <project_dir>/eps32_host/lib/fmap/fmap.h - Helper mapping utilities interface.
- <project_dir>/eps32_host/lib/fmap/fmap.cpp - Helper mapping utilities implementation.
- <project_dir>/eps32_host/lib/oled_lib/oled_lib.h - OLED interface.
- <project_dir>/eps32_host/lib/oled_lib/oled_lib.cpp - OLED implementation.
- <project_dir>/eps32_host/lib/pulse_lib/pulse_lib.h - Pulse generation interface.
- <project_dir>/eps32_host/lib/pulse_lib/pulse_lib.cpp - Pulse generation implementation.
- <project_dir>/eps32_host/lib/qc_lib/qc_7366_lib.h - QC7366 counter interface.
- <project_dir>/eps32_host/lib/qc_lib/qc_7366_lib.cpp - QC7366 counter implementation.
- <project_dir>/eps32_host/lib/spi_lib/spi_lib.h - SPI helper interface.
- <project_dir>/eps32_host/lib/spi_lib/spi_lib.cpp - SPI helper implementation.
- <project_dir>/eps32_host/lib/usb_wifi_switch/usb_wifi_switch.h - USB/WiFi mode switch interface.
- <project_dir>/eps32_host/lib/usb_wifi_switch/usb_wifi_switch.cpp - USB/WiFi mode switch implementation.
- <project_dir>/eps32_host/lib/WifiConfigureSupport/wifi_network_config.h - WiFi configuration interface.
- <project_dir>/eps32_host/lib/WifiConfigureSupport/wifi_network_config.cpp - WiFi configuration implementation.

### Web assets (eps32_host/data)

- <project_dir>/eps32_host/data/wifimanager.html - WiFi manager page.
- <project_dir>/eps32_host/data/style.css - WiFi manager styles.
- <project_dir>/eps32_host/data/style.css.gz - Pre-compressed CSS for the web UI.

## Python client (python_client)

- <project_dir>/python_client/requirements.txt - Python dependencies.
- <project_dir>/python_client/__init__.py - Package entry point.

### Core library (python_client/library)

- <project_dir>/python_client/library/config.py - Runtime configuration and constants.
- <project_dir>/python_client/library/debug_utility.py - Debug helpers.
- <project_dir>/python_client/library/rpc_client.py - RPC client implementation.
- <project_dir>/python_client/library/transport.py - USB/WiFi transport layer.
- <project_dir>/python_client/library/__init__.py - Library exports.

### GUI application (python_client/nodeMCU_gui)

- <project_dir>/python_client/nodeMCU_gui/nodeMCU_gui.py - Tkinter GUI entry point.
- <project_dir>/python_client/nodeMCU_gui/gpio_tab.py - GPIO controls.
- <project_dir>/python_client/nodeMCU_gui/system_tab.py - System info and utilities.
- <project_dir>/python_client/nodeMCU_gui/pwm_tab.py - PWM controls.
- <project_dir>/python_client/nodeMCU_gui/adc_tab.py - ADC tools.
- <project_dir>/python_client/nodeMCU_gui/dac_tab.py - DAC tools.
- <project_dir>/python_client/nodeMCU_gui/dio_tab.py - Digital IO expander tools.
- <project_dir>/python_client/nodeMCU_gui/oled_tab.py - OLED controls.
- <project_dir>/python_client/nodeMCU_gui/pulse_tab.py - Pulse generator tools.
- <project_dir>/python_client/nodeMCU_gui/qc_tab.py - QC7366 counter tools.
- <project_dir>/python_client/nodeMCU_gui/__init__.py - GUI package init.

### Example scripts (python_client/examples)

- <project_dir>/python_client/examples/example_usage.py - Basic API usage examples.
- <project_dir>/python_client/examples/advanced_example.py - Extended monitoring examples.
- <project_dir>/python_client/examples/test_debug.py - Debug utilities.
- <project_dir>/python_client/examples/test_debug.log - Example debug output.

### Debug documentation (python_client/documentation)

- <project_dir>/python_client/documentation/DEBUG_GUIDE.md - Debug workflow guidance.
- <project_dir>/python_client/documentation/DEBUG_SUMMARY.md - Debug summary.
- <project_dir>/python_client/documentation/QUICKREF_DEBUG.md - Debug quick reference.

### Portal GUI (python_client/portaal_robot)

- <project_dir>/python_client/portaal_robot/portal_gui.py - Portal GUI application.
- <project_dir>/python_client/portaal_robot/portal_config.yaml - Portal configuration.
- <project_dir>/python_client/portaal_robot/portaalrobot.jpg - Portal asset image.

## Other folders

- <project_dir>/NodeMCU - Additional NodeMCU assets (contents not indexed here).

## Generated and local-only folders

These directories are environment or tool specific and typically not part of the source of truth.

- <project_dir>/.git - Git metadata.
- <project_dir>/.venv - Local Python virtual environment.
- <project_dir>/eps32_host/.pio - PlatformIO build outputs.
- <project_dir>/eps32_host/.vscode - Editor settings for the firmware project.
- <project_dir>/eps32_host/.idea - IDE configuration.
- <project_dir>/python_client/.venv - Local Python virtual environment.
- <project_dir>/python_client/.idea - IDE configuration.
- <project_dir>/python_client/library/__pycache__ - Python bytecode cache.
- <project_dir>/python_client/nodeMCU_gui/__pycache__ - Python bytecode cache.
