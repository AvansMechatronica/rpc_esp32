#ifndef RPC_CONFIG_H
#define RPC_CONFIG_H

// Communication mode
#define COMM_USB 0
#define COMM_WIFI 1

// Current communication mode ==> Defined in platformio.ini
//#define CONFIG_COMM_MODE COMM_USB
//#define CONFIG_COMM_MODE COMM_WIFI

// WiFi configuration (used when COMM_WIFI mode is selected)
// Use these default values if WIFI_CONFIGURE_SERVER is not defined
#define CONFIG_WIFI_SSID "ESP32_RPC"
#define CONFIG_WIFI_PASSWORD "password123"

#define CONFIG_WIFI_PORT 5000

// USB/Serial configuration
#define CONFIG_BAUD_RATE 115200

// When 0, suppress non-JSON Serial logs so the RPC stream is clean.
// Set to 1 to enable human-readable logs on Serial.
#define RPC_SERIAL_LOGS 0

// RPC Protocol version
#define RPC_VERSION 1

// Result codes
#define RPC_OK 0
#define RPC_ERROR_INVALID_COMMAND 1
#define RPC_ERROR_INVALID_PARAMS 2
#define RPC_ERROR_TIMEOUT 3
#define RPC_ERROR_EXECUTION 4
#define RPC_ERROR_NOT_SUPPORTED 5

// Pulse library configuration
#define NUMBER_OF_PULSE_LIB_INSTANCES 4

#endif
