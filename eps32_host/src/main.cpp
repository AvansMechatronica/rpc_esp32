#include <Arduino.h>
#include <WiFi.h>
#include "rpc_server.h"
#include "config.h"
#include "wifi_network_config.h"

RpcServer rpc_server;

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n\nESP32 RPC Server Starting...");
  
  // Initialize RPC server
  rpc_server.begin();
  
  // Initialize WiFi if enabled
  if (CONFIG_COMM_MODE == COMM_WIFI) {
    Serial.println("Connecting to WiFi...");

    WiFi.setHostname("ESP32_RPC_Server");
#if defined WIFI_CONFIGURE_SERVER
    NETWORK_CONFIG network_config;

    if (!configureNetwork(false, &network_config)) {
      Serial.println("Failed to configure network");
    }
    WiFi.begin(network_config.ssid.c_str(), network_config.password.c_str());
#else
    
      WiFi.begin(CONFIG_WIFI_SSID, CONFIG_WIFI_PASSWORD);
#endif
    
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 20) {
      delay(500);
      Serial.print(".");
      attempts++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
      Serial.println("\nWiFi connected!");
      Serial.print("IP address: ");
      Serial.println(WiFi.localIP());
      Serial.printf("Listening on port %d\n", CONFIG_WIFI_PORT);
    } else {
      Serial.println("\nWiFi connection failed!");
    }
    Serial.println("RPC Server ready. Waiting for commands...");
  }
  
}

void loop() {
  // USB/Serial communication handled by RPC server


  if (CONFIG_COMM_MODE == COMM_USB) {
    rpc_server.handle_serial();
  } else if (CONFIG_COMM_MODE == COMM_WIFI) {
    // For WiFi, also handle serial commands
    rpc_server.handle_wifi();
  }
  
  // Handle pulse ticks for async pulse generation
  rpc_server.handlePulseTicks();
  
  delay(10);
}