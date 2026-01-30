#ifndef RPC_SERVER_H
#define RPC_SERVER_H

#include <Arduino.h>
#include <ArduinoJson.h>
#include "config.h"
#include "pulse_lib.h"
#include <WiFi.h>

class RpcServer {

public:
  RpcServer();
  void begin();
  void handle_serial();
  void handle_wifi();
  void handlePulseTicks();  // Process pulse ticks for all active channels
  
private:
  DynamicJsonDocument request_doc{2048};
  DynamicJsonDocument response_doc{2048};
  DynamicJsonDocument response_data{1024};  // Storage for response data

  PulseLib pulseLibChannels[NUMBER_OF_PULSE_LIB_INSTANCES];
  
  // WiFi TCP Server
  WiFiServer* tcp_server;
  WiFiClient tcp_client;
  bool tcp_server_started;
  
  // RPC Handler methods
  int execute_command(const char* method, JsonObject params);
  void send_response(int result_code, const char* message = "", JsonObject data = JsonObject());
  void send_response_tcp(int result_code, const char* message = "", JsonObject data = JsonObject());
  
  // GPIO functions
  int rpc_pinMode(JsonObject params);
  int rpc_digitalWrite(JsonObject params);
  int rpc_digitalRead(JsonObject params);
  int rpc_analogWrite(JsonObject params);
  int rpc_analogRead(JsonObject params);
  
  // System functions
  int rpc_delay(JsonObject params);
  int rpc_getMillis(JsonObject params);
  int rpc_getFreeMem(JsonObject params);
  int rpc_getChipID(JsonObject params);
  
  // I2C functions
  int rpc_i2c_begin(JsonObject params);
  int rpc_i2c_write(JsonObject params);
  int rpc_i2c_read(JsonObject params);
  
  // PWM/Analog functions
  int rpc_ledcSetup(JsonObject params);
  int rpc_ledcWrite(JsonObject params);
  
  // Pulse library functions
  int rpc_pulseBegin(JsonObject params);
  int rpc_pulse(JsonObject params);
  int rpc_pulseAsync(JsonObject params);
  int rpc_isPulsing(JsonObject params);
  int rpc_getRemainingPulses(JsonObject params);
  int rpc_stopPulse(JsonObject params);
  int rpc_generatePulses(JsonObject params);
  int rpc_generatePulsesAsync(JsonObject params);

#if defined INCLUDE_OLED_DISPLAY
  // OLED library functions
  int rpc_oledClear(JsonObject params);
  int rpc_oledWriteLine(JsonObject params);
#endif
  // Utility
  String getMethodName(const char* method);
  bool parseRequest(const String& request_str);
};

#endif
