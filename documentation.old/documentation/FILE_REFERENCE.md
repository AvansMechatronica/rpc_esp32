## File Reference - rpc_esp32

This document is a complete, current index of files and folders in the workspace. It focuses on structure and purpose.

## Top-level documentation

- [README.md](README.md) - Main project overview and Python client usage.
- [QUICKSTART.md](QUICKSTART.md) - Quick start steps and example workflows.
- [TECHNICAL_REFERENCE.md](TECHNICAL_REFERENCE.md) - Architecture and protocol details.
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Build summary and feature list.
- [FILE_REFERENCE.md](FILE_REFERENCE.md) - This index.

## ESP32 firmware (eps32_host)

- [eps32_host/platformio.ini](eps32_host/platformio.ini) - PlatformIO build configuration.
- [eps32_host/src/main.cpp](eps32_host/src/main.cpp) - Firmware entry point.
- [eps32_host/include/README](eps32_host/include/README) - Notes for the include folder.
- [eps32_host/test/README](eps32_host/test/README) - Test folder notes.

### Core firmware libraries (eps32_host/lib)

- [eps32_host/lib/config.h](eps32_host/lib/config.h) - Firmware configuration and result codes.
- [eps32_host/lib/bits.h](eps32_host/lib/bits.h) - Bit utilities and helpers.
- [eps32_host/lib/README](eps32_host/lib/README) - Library notes.

### RPC server library (eps32_host/lib/rpc_server)

- [eps32_host/lib/rpc_server/library.properties](eps32_host/lib/rpc_server/library.properties) - Arduino library metadata.
- [eps32_host/lib/rpc_server/include/rpc_config.h](eps32_host/lib/rpc_server/include/rpc_config.h) - RPC configuration definitions.
- [eps32_host/lib/rpc_server/include/rpc_server.h](eps32_host/lib/rpc_server/include/rpc_server.h) - RPC server interface.
- [eps32_host/lib/rpc_server/src/rpc_server.cpp](eps32_host/lib/rpc_server/src/rpc_server.cpp) - RPC server implementation.

### Optional hardware libraries (eps32_host/lib)

- [eps32_host/lib/adc_lib/adc_3208_lib.h](eps32_host/lib/adc_lib/adc_3208_lib.h) - MCP3208 ADC interface.
- [eps32_host/lib/adc_lib/adc_3208_lib.cpp](eps32_host/lib/adc_lib/adc_3208_lib.cpp) - MCP3208 ADC implementation.
- [eps32_host/lib/dac_lib/dac_4922_lib.h](eps32_host/lib/dac_lib/dac_4922_lib.h) - MCP4922 DAC interface.
- [eps32_host/lib/dac_lib/dac_4922_lib.cpp](eps32_host/lib/dac_lib/dac_4922_lib.cpp) - MCP4922 DAC implementation.
- [eps32_host/lib/dio_lib/dio_lib.h](eps32_host/lib/dio_lib/dio_lib.h) - Digital IO expander interface.
- [eps32_host/lib/dio_lib/dio_lib.cpp](eps32_host/lib/dio_lib/dio_lib.cpp) - Digital IO expander implementation.
- [eps32_host/lib/fmap/fmap.h](eps32_host/lib/fmap/fmap.h) - Helper mapping utilities interface.
- [eps32_host/lib/fmap/fmap.cpp](eps32_host/lib/fmap/fmap.cpp) - Helper mapping utilities implementation.
- [eps32_host/lib/oled_lib/oled_lib.h](eps32_host/lib/oled_lib/oled_lib.h) - OLED interface.
- [eps32_host/lib/oled_lib/oled_lib.cpp](eps32_host/lib/oled_lib/oled_lib.cpp) - OLED implementation.
- [eps32_host/lib/pulse_lib/pulse_lib.h](eps32_host/lib/pulse_lib/pulse_lib.h) - Pulse generation interface.
- [eps32_host/lib/pulse_lib/pulse_lib.cpp](eps32_host/lib/pulse_lib/pulse_lib.cpp) - Pulse generation implementation.
- [eps32_host/lib/qc_lib/qc_7366_lib.h](eps32_host/lib/qc_lib/qc_7366_lib.h) - QC7366 counter interface.
- [eps32_host/lib/qc_lib/qc_7366_lib.cpp](eps32_host/lib/qc_lib/qc_7366_lib.cpp) - QC7366 counter implementation.
- [eps32_host/lib/spi_lib/spi_lib.h](eps32_host/lib/spi_lib/spi_lib.h) - SPI helper interface.
- [eps32_host/lib/spi_lib/spi_lib.cpp](eps32_host/lib/spi_lib/spi_lib.cpp) - SPI helper implementation.
- [eps32_host/lib/usb_wifi_switch/usb_wifi_switch.h](eps32_host/lib/usb_wifi_switch/usb_wifi_switch.h) - USB/WiFi mode switch interface.
- [eps32_host/lib/usb_wifi_switch/usb_wifi_switch.cpp](eps32_host/lib/usb_wifi_switch/usb_wifi_switch.cpp) - USB/WiFi mode switch implementation.
- [eps32_host/lib/WifiConfigureSupport/wifi_network_config.h](eps32_host/lib/WifiConfigureSupport/wifi_network_config.h) - WiFi configuration interface.
- [eps32_host/lib/WifiConfigureSupport/wifi_network_config.cpp](eps32_host/lib/WifiConfigureSupport/wifi_network_config.cpp) - WiFi configuration implementation.

### Web assets (eps32_host/data)

- [eps32_host/data/wifimanager.html](eps32_host/data/wifimanager.html) - WiFi manager page.
- [eps32_host/data/style.css](eps32_host/data/style.css) - WiFi manager styles.
- [eps32_host/data/style.css.gz](eps32_host/data/style.css.gz) - Pre-compressed CSS for the web UI.

## Python client (python_client)

- [python_client/requirements.txt](python_client/requirements.txt) - Python dependencies.
- [python_client/__init__.py](python_client/__init__.py) - Package entry point.

### Core library (python_client/library)

- [python_client/library/config.py](python_client/library/config.py) - Runtime configuration and constants.
- [python_client/library/debug_utility.py](python_client/library/debug_utility.py) - Debug helpers.
- [python_client/library/rpc_client.py](python_client/library/rpc_client.py) - RPC client implementation.
- [python_client/library/transport.py](python_client/library/transport.py) - USB/WiFi transport layer.
- [python_client/library/__init__.py](python_client/library/__init__.py) - Library exports.

### GUI application (python_client/nodeMCU_gui)

- [python_client/nodeMCU_gui/nodeMCU_gui.py](python_client/nodeMCU_gui/nodeMCU_gui.py) - Tkinter GUI entry point.
- [python_client/nodeMCU_gui/gpio_tab.py](python_client/nodeMCU_gui/gpio_tab.py) - GPIO controls.
- [python_client/nodeMCU_gui/system_tab.py](python_client/nodeMCU_gui/system_tab.py) - System info and utilities.
- [python_client/nodeMCU_gui/pwm_tab.py](python_client/nodeMCU_gui/pwm_tab.py) - PWM controls.
- [python_client/nodeMCU_gui/adc_tab.py](python_client/nodeMCU_gui/adc_tab.py) - ADC tools.
- [python_client/nodeMCU_gui/dac_tab.py](python_client/nodeMCU_gui/dac_tab.py) - DAC tools.
- [python_client/nodeMCU_gui/dio_tab.py](python_client/nodeMCU_gui/dio_tab.py) - Digital IO expander tools.
- [python_client/nodeMCU_gui/oled_tab.py](python_client/nodeMCU_gui/oled_tab.py) - OLED controls.
- [python_client/nodeMCU_gui/pulse_tab.py](python_client/nodeMCU_gui/pulse_tab.py) - Pulse generator tools.
- [python_client/nodeMCU_gui/qc_tab.py](python_client/nodeMCU_gui/qc_tab.py) - QC7366 counter tools.
- [python_client/nodeMCU_gui/__init__.py](python_client/nodeMCU_gui/__init__.py) - GUI package init.

### Example scripts (python_client/examples)

- [python_client/examples/example_usage.py](python_client/examples/example_usage.py) - Basic API usage examples.
- [python_client/examples/advanced_example.py](python_client/examples/advanced_example.py) - Extended monitoring examples.
- [python_client/examples/test_debug.py](python_client/examples/test_debug.py) - Debug utilities.
- [python_client/examples/test_debug.log](python_client/examples/test_debug.log) - Example debug output.

### Debug documentation (python_client/documentation)

- [python_client/documentation/DEBUG_GUIDE.md](python_client/documentation/DEBUG_GUIDE.md) - Debug workflow guidance.
- [python_client/documentation/DEBUG_SUMMARY.md](python_client/documentation/DEBUG_SUMMARY.md) - Debug summary.
- [python_client/documentation/QUICKREF_DEBUG.md](python_client/documentation/QUICKREF_DEBUG.md) - Debug quick reference.

### Portal GUI (python_client/portaal_robot)

- [python_client/portaal_robot/portal_gui.py](python_client/portaal_robot/portal_gui.py) - Portal GUI application.
- [python_client/portaal_robot/portal_config.yaml](python_client/portaal_robot/portal_config.yaml) - Portal configuration.
- [python_client/portaal_robot/portaalrobot.jpg](python_client/portaal_robot/portaalrobot.jpg) - Portal asset image.

## Other folders

- [NodeMCU](NodeMCU) - Additional NodeMCU assets (contents not indexed here).

## Generated and local-only folders

These directories are environment or tool specific and typically not part of the source of truth.

- [.git](.git) - Git metadata.
- [.venv](.venv) - Local Python virtual environment.
- [eps32_host/.pio](eps32_host/.pio) - PlatformIO build outputs.
- [eps32_host/.vscode](eps32_host/.vscode) - Editor settings for the firmware project.
- [eps32_host/.idea](eps32_host/.idea) - IDE configuration.
- [python_client/.venv](python_client/.venv) - Local Python virtual environment.
- [python_client/.idea](python_client/.idea) - IDE configuration.
- [python_client/library/__pycache__](python_client/library/__pycache__) - Python bytecode cache.
- [python_client/nodeMCU_gui/__pycache__](python_client/nodeMCU_gui/__pycache__) - Python bytecode cache.
