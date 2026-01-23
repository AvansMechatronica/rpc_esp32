#include <Arduino.h>
#include <WiFi.h>
#include "rpc_server.h"
#include "config.h"

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
    WiFi.begin(CONFIG_WIFI_SSID, CONFIG_WIFI_PASSWORD);
    
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
    } else {
      Serial.println("\nWiFi connection failed!");
    }
  }
  
  Serial.println("RPC Server ready. Waiting for commands...");
}

void loop() {
  // USB/Serial communication handled by RPC server
  if (CONFIG_COMM_MODE == COMM_USB) {
    rpc_server.handle_serial();
  }
  
  delay(10);
}