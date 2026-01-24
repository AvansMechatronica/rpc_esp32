#ifndef RPC_CONFIG_H
#define RPC_CONFIG_H

// Communication mode
#define COMM_USB 0
#define COMM_WIFI 1

// Current communication mode
//#define CONFIG_COMM_MODE COMM_USB
#define CONFIG_COMM_MODE COMM_WIFI

// WiFi configuration (used when COMM_WIFI mode is selected)
#define CONFIG_WIFI_SSID "ESP32_RPC"
#define CONFIG_WIFI_PASSWORD "password123"
#define CONFIG_WIFI_PORT 5000

// USB/Serial configuration
#define CONFIG_BAUD_RATE 115200

// RPC Protocol version
#define RPC_VERSION 1

// Result codes
#define RPC_OK 0
#define RPC_ERROR_INVALID_COMMAND 1
#define RPC_ERROR_INVALID_PARAMS 2
#define RPC_ERROR_TIMEOUT 3
#define RPC_ERROR_EXECUTION 4
#define RPC_ERROR_NOT_SUPPORTED 5

#endif
