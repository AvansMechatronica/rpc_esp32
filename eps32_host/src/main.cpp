#include <Arduino.h>
#include <WiFi.h>
#include "rpc_server.h"
#include "config.h"
#include "wifi_network_config.h"
#include "usb_wifi_switch.h"
#if defined INCLUDE_OLED_DISPLAY
#include "oled_lib.h"
#endif

#if defined INCLUDE_DAC_4922_LIB || defined INCLUDE_ADC_3208_LIB
#include "spi_lib.h"
spi spi_bus;
#endif

#if defined INCLUDE_DAC_4922_LIB
#include "dac_4922_lib.h"
dac4922 dac;
#endif

#if INCLUDE_ADC_3208_LIB
#include "adc_3208_lib.h"
adc8208 adc;
#endif

#if defined INCLUDE_DIO_LIB
#include "dio_lib.h"
dio digital_io;
#endif

RpcServer rpc_server;

#if defined INCLUDE_OLED_DISPLAY
oledDisplay  oled_Display;
#endif


//#define WIFI_CONFIGURE_BUTTON_PIN 5  // GPIO pin for forcing WiFi configuration mode
#define COMM_MODE_BUTTON_PIN 4     // GPIO pin for toggling communication mode

bool wifi_mode = false;

void setup() {
  Serial.begin(115200);
  delay(1000);

#if defined INCLUDE_OLED_DISPLAY
  bool oledOK  = oled_Display.Init();
  if(!oledOK) {
#if RPC_SERIAL_LOGS
    Serial.println("OLED Init failed!");
#endif
  }
  oled_Display.Clear();
	oled_Display.WriteLine(0, "ESP32 RPC", ALIGN_CENTER);
	oled_Display.WriteLine(1, "Server",  ALIGN_CENTER);
	oled_Display.WriteLine(2, "V0.6",  		ALIGN_CENTER);
	oled_Display.WriteLine(3, "Server Starting...",  		ALIGN_CENTER);
  delay(2000);
#endif  

#if defined INCLUDE_DAC_4922_LIB || defined INCLUDE_ADC_3208_LIB
  spi_bus.Init();
#endif

#if defined INCLUDE_DAC_4922_LIB
  dac.Init(&spi_bus);
#endif

#if defined INCLUDE_ADC_3208_LIB
  adc.Init(&spi_bus);
#endif

#if defined INCLUDE_DIO_LIB
  digital_io.Init();
#endif

#if RPC_SERIAL_LOGS
  Serial.println("\n\nESP32 RPC Server Starting...");
#endif
  wifi_mode = check_wifi_mode();
  //pinMode(WIFI_CONFIGURE_BUTTON_PIN, INPUT_PULLUP);
  pinMode(COMM_MODE_BUTTON_PIN, INPUT_PULLUP);

  // Check if communication mode toggle button is pressed
  if (digitalRead(COMM_MODE_BUTTON_PIN) == LOW) {
#if RPC_SERIAL_LOGS
    Serial.println("Communication mode toggle button pressed. Toggling mode.");
#endif
    toggle_usb_wifi_mode();
    wifi_mode = check_wifi_mode();
  }

  // Initialize RPC server
  rpc_server.begin();
  
  // Initialize WiFi if enabled
  if (wifi_mode) {
#if RPC_SERIAL_LOGS
    Serial.println("Connecting to WiFi...");
#endif
#if defined INCLUDE_OLED_DISPLAY
    oled_Display.Clear();
    oled_Display.WriteLine(0, "ESP32 RPC", ALIGN_CENTER);
    oled_Display.WriteLine(1, "Connecting to ",  ALIGN_CENTER);
    oled_Display.WriteLine(2, "WiFi...",  		ALIGN_CENTER);
#endif
    WiFi.setHostname("ESP32_RPC_Server");
#if defined WIFI_CONFIGURE_SERVER
    NETWORK_CONFIG network_config;

    bool force_network_configure = adc.IsButtonPressed(1);  // Check if button 1 is pressed to force network configuration mode
    if (!configureNetwork(force_network_configure, &network_config)) {
    #if RPC_SERIAL_LOGS
      Serial.println("Failed to configure network");
    #endif
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
    #if RPC_SERIAL_LOGS
      Serial.print(".");
    #endif
      attempts++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
    #if RPC_SERIAL_LOGS
      Serial.println("\nWiFi connected!");
      Serial.print("IP address: ");
      Serial.println(WiFi.localIP());
      Serial.printf("Listening on port %d\n", CONFIG_WIFI_PORT);
    #endif
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
    #if RPC_SERIAL_LOGS
      Serial.println("\nWiFi connection failed!");
    #endif
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
  #if RPC_SERIAL_LOGS
    Serial.println("RPC Server ready. Waiting for commands...");
  #endif
    
  }
#if defined INCLUDE_OLED_DISPLAY
  oled_Display.Clear();
	oled_Display.WriteLine(0, "ESP32 RPC", ALIGN_CENTER);
	oled_Display.WriteLine(1, "Server Ready",  ALIGN_CENTER);
  if (wifi_mode) {
    oled_Display.WriteLine(2, "WiFi Connection",  		ALIGN_CENTER);
    char text_buffer[32];
    snprintf(text_buffer, sizeof(text_buffer), "IP: %s", WiFi.localIP().toString().c_str());
    oled_Display.WriteLine(3, text_buffer,  ALIGN_CENTER);
  }
  else
    oled_Display.WriteLine(3, "USB Connection",  		ALIGN_CENTER);
#endif
  Serial.flush();
}

void loop() {

  if (!wifi_mode) {
    rpc_server.handle_serial();
  } else {
    // For WiFi, also handle serial commands
    rpc_server.handle_wifi();
  }
  
  // Handle pulse ticks for async pulse generation
  rpc_server.handlePulseTicks();
  
  delay(10);
}