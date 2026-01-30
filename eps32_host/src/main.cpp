#include <Arduino.h>
#include <WiFi.h>
#include "rpc_server.h"
#include "config.h"
#include "wifi_network_config.h"
#if defined INCLUDE_OLED_DISPLAY
#include "oled.h"
#endif

RpcServer rpc_server;

#if defined INCLUDE_OLED_DISPLAY
oledDisplay  oled_Display;
#endif


void setup() {
  Serial.begin(115200);
  delay(1000);

#if defined INCLUDE_OLED_DISPLAY
  bool oledOK  = oled_Display.Init();
  if(!oledOK) {
    Serial.println("OLED Init failed!");
  }
  oled_Display.Clear();
	oled_Display.WriteLine(0, "ESP32 RPC", ALIGN_CENTER);
	oled_Display.WriteLine(1, "Server",  ALIGN_CENTER);
	oled_Display.WriteLine(2, "V0.6",  		ALIGN_CENTER);
	oled_Display.WriteLine(3, "Server Starting...",  		ALIGN_CENTER);
  delay(2000);
#endif  
  Serial.println("\n\nESP32 RPC Server Starting...");
  
  // Initialize RPC server
  rpc_server.begin();
  
  // Initialize WiFi if enabled
  if (CONFIG_COMM_MODE == COMM_WIFI) {
    Serial.println("Connecting to WiFi...");
#if defined INCLUDE_OLED_DISPLAY
    oled_Display.Clear();
    oled_Display.WriteLine(0, "ESP32 RPC", ALIGN_CENTER);
    oled_Display.WriteLine(1, "Connecting to ",  ALIGN_CENTER);
    oled_Display.WriteLine(2, "WiFi...",  		ALIGN_CENTER);
#endif
    WiFi.setHostname("ESP32_RPC_Server");
#if defined WIFI_CONFIGURE_SERVER
    NETWORK_CONFIG network_config;

    if (!configureNetwork(false, &network_config)) {
      Serial.println("Failed to configure network");
#if defined INCLUDE_OLED_DISPLAY
      oled_Display.Clear();
      oled_Display.WriteLine(0, "ESP32 RPC", ALIGN_CENTER);
      oled_Display.WriteLine(1, "Failed to",  ALIGN_CENTER);
      oled_Display.WriteLine(2, "configure network",  	ALIGN_CENTER);
      oled_Display.WriteLine(3, "Restarting...",  	ALIGN_CENTER);
#endif
      delay(3000);
      ESP.restart();
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
#if defined INCLUDE_OLED_DISPLAY
      char text_buffer[32];
      oled_Display.Clear();
      oled_Display.WriteLine(0, "ESP32 RPC", ALIGN_CENTER);
      oled_Display.WriteLine(1, "WiFi connected",  ALIGN_CENTER);
      snprintf(text_buffer, sizeof(text_buffer), "IP: %s", WiFi.localIP().toString().c_str());
      oled_Display.WriteLine(2, text_buffer,  ALIGN_CENTER);
      sniprintf(text_buffer, sizeof(text_buffer), "Port: %d", CONFIG_WIFI_PORT);
      oled_Display.WriteLine(3, text_buffer,  ALIGN_CENTER);
      delay(3000);
#endif

    } else {
      Serial.println("\nWiFi connection failed!");
#if defined INCLUDE_OLED_DISPLAY
      oled_Display.Clear();
      oled_Display.WriteLine(0, "ESP32 RPC", ALIGN_CENTER);
      oled_Display.WriteLine(1, "WiFi",  ALIGN_CENTER);
      oled_Display.WriteLine(2, "connection failed",  	ALIGN_CENTER);
      oled_Display.WriteLine(3, "Restarting...",  	ALIGN_CENTER);
#endif
      delay(3000);
      ESP.restart();
    }
    Serial.println("RPC Server ready. Waiting for commands...");
    
  }
#if defined INCLUDE_OLED_DISPLAY
  oled_Display.Clear();
	oled_Display.WriteLine(0, "ESP32 RPC", ALIGN_CENTER);
	oled_Display.WriteLine(1, "Server Ready",  ALIGN_CENTER);
#if CONFIG_COMM_MODE == COMM_WIFI
  oled_Display.WriteLine(2, "WiFi Connection",  		ALIGN_CENTER);
  char text_buffer[32];
  snprintf(text_buffer, sizeof(text_buffer), "IP: %s", WiFi.localIP().toString().c_str());
  oled_Display.WriteLine(3, text_buffer,  ALIGN_CENTER);

#else   
  oled_Display.WriteLine(3, "USB Connection",  		ALIGN_CENTER);
#endif
#endif
  
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