
#if defined INCLUDE_OLED_DISPLAY
#include "oled_lib.h"
extern oledDisplay oled_Display;
#endif
#include "dac_4922_lib.h"
extern dac4922 dac;
#if defined INCLUDE_ADC_3208_LIB
#include "adc_3208_lib.h"
extern adc8208 adc;
#endif
#if defined INCLUDE_DIO_LIB
#include "dio_lib.h"
extern dio digital_io;
#endif
#if defined INCLUDE_QC_7366_LIB
#include "qc_7366_lib.h"
extern qc7366 qc;
#endif
#include "rpc_server.h"

RpcServer::RpcServer() {
  tcp_server = nullptr;
  tcp_server_started = false;
}

void RpcServer::begin() {
  Serial.begin(CONFIG_BAUD_RATE);
  
  // Initialize WiFi TCP server if needed
  // This will be started after WiFi is connected in main.cpp
  tcp_server = new WiFiServer(CONFIG_WIFI_PORT);
  tcp_server_started = false;
}

void RpcServer::handlePulseTicks() {
  // Update all pulse channels for async pulse generation
  for (int i = 0; i < NUMBER_OF_PULSE_LIB_INSTANCES; i++) {
    pulseLibChannels[i].tick();
  }
}

void RpcServer::handle_serial() {
  if (Serial.available()) {
    String request_str = Serial.readStringUntil('\n');
    request_str.trim();
    
    if (request_str.length() > 0) {
      if (parseRequest(request_str)) {
        const char* method = request_doc["method"];
        JsonObject params = request_doc["params"];
        
        // Clear response data before executing command
        response_data.clear();
        
        int result = execute_command(method, params);
        
        // Send response with data if any was set
        if (response_data.size() > 0) {
          send_response(result, "", response_data.as<JsonObject>());
        } else {
          send_response(result);
        }
      } else {
        send_response(RPC_ERROR_INVALID_COMMAND, "Invalid JSON format");
      }
    }
  }
}

void RpcServer::handle_wifi() {
  if (tcp_server == nullptr) {
    return;
  }

  // Start TCP server once WiFi is connected
  if (WiFi.status() == WL_CONNECTED && !tcp_server_started && tcp_server != nullptr) {
    tcp_server->begin();
    tcp_server_started = true;
  }

  // Check for new client connections
  if (!tcp_client || !tcp_client.connected()) {
    tcp_client = tcp_server->available();
    if (!tcp_client) {
#if RPC_SERIAL_LOGS
      Serial.println("[DEBUG] No client available.");
#endif
    } else {
#if RPC_SERIAL_LOGS
      Serial.println("[DEBUG] New client connected.");
#endif
    }
  }

  // Handle connected client
  if (tcp_client && tcp_client.connected()) {
    // Check if data is available from the TCP client
    if (tcp_client.available()) {
      String request_str = tcp_client.readStringUntil('\n');
      request_str.trim();

      if (request_str.length() > 0) {
#if RPC_SERIAL_LOGS
        Serial.printf("[DEBUG] Received request: %s\n", request_str.c_str());
#endif
        if (parseRequest(request_str)) {
          const char* method = request_doc["method"];
          JsonObject params = request_doc["params"];

          // Clear response data before executing command
          response_data.clear();

          int result = execute_command(method, params);

          // Send response via TCP
          if (response_data.size() > 0) {
            send_response_tcp(result, "", response_data.as<JsonObject>());
          } else {
            send_response_tcp(result);
          }
        } else {
          send_response_tcp(RPC_ERROR_INVALID_COMMAND, "Invalid JSON format");
        }
      }
    }
    // Check if client is still connected after handling
    if (!tcp_client.connected()) {
#if RPC_SERIAL_LOGS
      Serial.println("[DEBUG] Client disconnected.");
#endif
    }
  } else {
    if (!tcp_server->hasClient()) {
      // No client connected, attempt to listen if server not started
      if (WiFi.status() == WL_CONNECTED) {
        tcp_server->begin();
      }
    }
  }
}

bool RpcServer::parseRequest(const String& request_str) {
  DeserializationError error = deserializeJson(request_doc, request_str);
  return error == DeserializationError::Ok;
}

int RpcServer::execute_command(const char* method, JsonObject params) {
  // OLED commands

  if (strcmp(method, "pinMode") == 0) {
    return rpc_pinMode(params);
  } else if (strcmp(method, "digitalWrite") == 0) {
    return rpc_digitalWrite(params);
  } else if (strcmp(method, "digitalRead") == 0) {
    return rpc_digitalRead(params);
  } else if (strcmp(method, "analogWrite") == 0) {
    return rpc_analogWrite(params);
  } else if (strcmp(method, "analogRead") == 0) {
    return rpc_analogRead(params);
  } else if (strcmp(method, "delay") == 0) {
    return rpc_delay(params);
  } else if (strcmp(method, "millis") == 0) {
    return rpc_getMillis(params);
  } else if (strcmp(method, "freeMem") == 0) {
    return rpc_getFreeMem(params);
  } else if (strcmp(method, "chipID") == 0) {
    return rpc_getChipID(params);
  } else if (strcmp(method, "ledcSetup") == 0) {
    return rpc_ledcSetup(params);
  } else if (strcmp(method, "ledcWrite") == 0) {
    return rpc_ledcWrite(params);
  } else if (strcmp(method, "pulseBegin") == 0) {
    return rpc_pulseBegin(params);
  } else if (strcmp(method, "pulse") == 0) {
    return rpc_pulse(params);
  } else if (strcmp(method, "pulseAsync") == 0) {
    return rpc_pulseAsync(params);
  } else if (strcmp(method, "isPulsing") == 0) {
    return rpc_isPulsing(params);
  } else if (strcmp(method, "getRemainingPulses") == 0) {
    return rpc_getRemainingPulses(params);
  } else if (strcmp(method, "stopPulse") == 0) {
    return rpc_stopPulse(params);
  } else if (strcmp(method, "generatePulses") == 0) {
    return rpc_generatePulses(params);
  } else if (strcmp(method, "generatePulsesAsync") == 0) {
    return rpc_generatePulsesAsync(params);
#if defined INCLUDE_ADC_3208_LIB
  } else if (strcmp(method, "adcReadRaw") == 0) {
    return rpc_adcReadRaw(params);
  } else if (strcmp(method, "adcReadVoltage") == 0) {
    return rpc_adcReadVoltage(params);
  } else if (strcmp(method, "isButtonPressed") == 0) {
    return rpc_isButtonPressed(params);
#endif
#if defined INCLUDE_DAC_4922_LIB
  } else if (strcmp(method, "dacSetVoltage") == 0) {
    return rpc_dacSetVoltage(params);
  } else if (strcmp(method, "dacSetVoltageAll") == 0) {
    return rpc_dacSetVoltageAll(params);
#endif
#if defined INCLUDE_DIO_LIB
  } else if (strcmp(method, "dioGetInput") == 0) {
    return rpc_dioGetInput(params);
  } else if (strcmp(method, "dioIsBitSet") == 0) {
    return rpc_dioIsBitSet(params);
  } else if (strcmp(method, "dioSetOutput") == 0) {
    return rpc_dioSetOutput(params);
  } else if (strcmp(method, "dioSetBit") == 0) {
    return rpc_dioSetBit(params);
  } else if (strcmp(method, "dioClearBit") == 0) {
    return rpc_dioClearBit(params);
  } else if (strcmp(method, "dioToggleBit") == 0) {
    return rpc_dioToggleBit(params);
#endif
#if defined INCLUDE_QC_7366_LIB
  } else if (strcmp(method, "qcEnableCounter") == 0) {
    return rpc_qcEnableCounter(params);
  } else if (strcmp(method, "qcDisableCounter") == 0) {
    return rpc_qcDisableCounter(params);
  } else if (strcmp(method, "qcClearCountRegister") == 0) {
    return rpc_qcClearCountRegister(params);
  } else if (strcmp(method, "qcReadCountRegister") == 0) {
    return rpc_qcReadCountRegister(params);
#endif
#if defined INCLUDE_OLED_DISPLAY
  } else if (strcmp(method, "oledClear") == 0) {
    return rpc_oledClear(params);
  } else if (strcmp(method, "oledWriteLine") == 0) {
    return rpc_oledWriteLine(params);
#endif
  } else {
    return RPC_ERROR_INVALID_COMMAND;
  }
}

void RpcServer::send_response(int result_code, const char* message, JsonObject data) {
  response_doc.clear();
  response_doc["result"] = result_code;
  response_doc["message"] = message;
  
  if (!data.isNull()) {
    response_doc["data"] = data;
  }
  
  String response;
  serializeJson(response_doc, response);
  Serial.println(response);
}

void RpcServer::send_response_tcp(int result_code, const char* message, JsonObject data) {
  response_doc.clear();
  response_doc["result"] = result_code;
  response_doc["message"] = message;
  
  if (!data.isNull()) {
    response_doc["data"] = data;
  }
  
  String response;
  serializeJson(response_doc, response);
  
  if (tcp_client.connected()) {
    tcp_client.println(response);
  }
}

// GPIO Functions
int RpcServer::rpc_pinMode(JsonObject params) {
  if (!params.containsKey("pin") || !params.containsKey("mode")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t pin = params["pin"];
  uint8_t mode = params["mode"];
  
  pinMode(pin, mode);
  return RPC_OK;
}

int RpcServer::rpc_digitalWrite(JsonObject params) {
  if (!params.containsKey("pin") || !params.containsKey("value")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t pin = params["pin"];
  uint8_t value = params["value"];
  
  // Ensure pin is set to OUTPUT mode before writing
  pinMode(pin, OUTPUT);
  digitalWrite(pin, value);
  return RPC_OK;
}

int RpcServer::rpc_digitalRead(JsonObject params) {
  if (!params.containsKey("pin")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t pin = params["pin"];
  
  // Only set pin mode if explicitly provided; otherwise read current pin state
  if (params.containsKey("mode")) {
    uint8_t mode = params["mode"];
    pinMode(pin, mode);
  }
  // Do NOT change pin mode during read - preserve the current pin configuration
  // (e.g., OUTPUT pins should stay OUTPUT to read the value being driven)
  
  int value = digitalRead(pin);
  
  response_data["value"] = value;
  
  return RPC_OK;
}

int RpcServer::rpc_analogWrite(JsonObject params) {
  if (!params.containsKey("pin") || !params.containsKey("value")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t pin = params["pin"];
  uint8_t value = params["value"];
  
  analogWrite(pin, value);
  return RPC_OK;
}

int RpcServer::rpc_analogRead(JsonObject params) {
  if (!params.containsKey("pin")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t pin = params["pin"];
  int value = analogRead(pin);
  
  response_data["value"] = value;
  
  return RPC_OK;
}

// System Functions
int RpcServer::rpc_delay(JsonObject params) {
  if (!params.containsKey("ms")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint32_t ms = params["ms"];
  delay(ms);
  
  return RPC_OK;
}

int RpcServer::rpc_getMillis(JsonObject params) {
  uint32_t ms = millis();
  
  response_data["millis"] = ms;
  
  return RPC_OK;
}

int RpcServer::rpc_getFreeMem(JsonObject params) {
  uint32_t free_mem = ESP.getFreeHeap();
  
  response_data["free_heap"] = free_mem;
  
  return RPC_OK;
}

int RpcServer::rpc_getChipID(JsonObject params) {
  uint32_t chip_id = ESP.getEfuseMac();
  
  response_data["chip_id"] = (uint32_t)(chip_id & 0xFFFFFFFF);
  
  return RPC_OK;
}

// PWM/Analog Functions
int RpcServer::rpc_ledcSetup(JsonObject params) {
  if (!params.containsKey("channel") || !params.containsKey("freq") || !params.containsKey("bits")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t channel = params["channel"];
  uint32_t freq = params["freq"];
  uint8_t bits = params["bits"];
  
  ledcSetup(channel, freq, bits);
  return RPC_OK;
}

int RpcServer::rpc_ledcWrite(JsonObject params) {
  if (!params.containsKey("channel") || !params.containsKey("duty")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t channel = params["channel"];
  uint32_t duty = params["duty"];
  
  ledcWrite(channel, duty);
  return RPC_OK;
}

// I2C Functions
int RpcServer::rpc_i2c_begin(JsonObject params) {
  // Placeholder for I2C begin
  return RPC_OK;
}

int RpcServer::rpc_i2c_write(JsonObject params) {
  // Placeholder for I2C write
  return RPC_OK;
}

int RpcServer::rpc_i2c_read(JsonObject params) {
  // Placeholder for I2C read
  return RPC_OK;
}

String RpcServer::getMethodName(const char* method) {
  return String(method);
}

// Pulse Library Functions
int RpcServer::rpc_pulseBegin(JsonObject params) {
  if (!params.containsKey("channel") || !params.containsKey("pin")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t channel = params["channel"];
  uint8_t pin = params["pin"];
  
  if (channel >= NUMBER_OF_PULSE_LIB_INSTANCES) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  pulseLibChannels[channel].begin(pin);
  return RPC_OK;
}

int RpcServer::rpc_pulse(JsonObject params) {
  if (!params.containsKey("channel") || !params.containsKey("duration_ms")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t channel = params["channel"];
  uint32_t duration_ms = params["duration_ms"];
  
  if (channel >= NUMBER_OF_PULSE_LIB_INSTANCES) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  pulseLibChannels[channel].pulse(duration_ms);
  return RPC_OK;
}

int RpcServer::rpc_pulseAsync(JsonObject params) {
  if (!params.containsKey("channel") || !params.containsKey("duration_ms")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t channel = params["channel"];
  uint32_t duration_ms = params["duration_ms"];
  
  if (channel >= NUMBER_OF_PULSE_LIB_INSTANCES) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  pulseLibChannels[channel].pulseAsync(duration_ms);
  return RPC_OK;
}

int RpcServer::rpc_isPulsing(JsonObject params) {
  if (!params.containsKey("channel")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t channel = params["channel"];
  
  if (channel >= NUMBER_OF_PULSE_LIB_INSTANCES) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  bool pulsing = pulseLibChannels[channel].isPulsing();
  response_data["pulsing"] = pulsing;
  
  return RPC_OK;
}

int RpcServer::rpc_stopPulse(JsonObject params) {
  if (!params.containsKey("channel")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t channel = params["channel"];
  
  if (channel >= NUMBER_OF_PULSE_LIB_INSTANCES) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  pulseLibChannels[channel].stopPulse();
  return RPC_OK;
}

int RpcServer::rpc_generatePulses(JsonObject params) {
  if (!params.containsKey("channel") || !params.containsKey("pulse_width_ms") || 
      !params.containsKey("pause_width_ms") || !params.containsKey("pulse_count")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t channel = params["channel"];
  uint32_t pulse_width_ms = params["pulse_width_ms"];
  uint32_t pause_width_ms = params["pause_width_ms"];
  uint32_t pulse_count = params["pulse_count"];
  
  if (channel >= NUMBER_OF_PULSE_LIB_INSTANCES) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  pulseLibChannels[channel].generetePulses(pulse_width_ms, pause_width_ms, pulse_count);
  return RPC_OK;
}

int RpcServer::rpc_generatePulsesAsync(JsonObject params) {
  if (!params.containsKey("channel") || !params.containsKey("pulse_width_ms") || 
      !params.containsKey("pause_width_ms") || !params.containsKey("pulse_count")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t channel = params["channel"];
  uint32_t pulse_width_ms = params["pulse_width_ms"];
  uint32_t pause_width_ms = params["pause_width_ms"];
  uint32_t pulse_count = params["pulse_count"];
  
  if (channel >= NUMBER_OF_PULSE_LIB_INSTANCES) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  pulseLibChannels[channel].generetePulsesAsync(pulse_width_ms, pause_width_ms, pulse_count);
  return RPC_OK;
}

int RpcServer::rpc_getRemainingPulses(JsonObject params) {
  if (!params.containsKey("channel")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t channel = params["channel"];
  
  if (channel >= NUMBER_OF_PULSE_LIB_INSTANCES) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  int remaining = pulseLibChannels[channel].getRemainingPulses();
  response_data["remaining"] = remaining;
  
  return RPC_OK;
}

#if defined INCLUDE_QC_7366_LIB
int RpcServer::rpc_qcEnableCounter(JsonObject params) {
  if (!params.containsKey("channel")) {
    return RPC_ERROR_INVALID_PARAMS;
  }

  uint8_t channel = params["channel"];

  if (channel > QC_MAX_CHANNEL) {
    return RPC_ERROR_INVALID_PARAMS;
  }

  qc.enableCounter(channel);
  return RPC_OK;
}

int RpcServer::rpc_qcDisableCounter(JsonObject params) {
  if (!params.containsKey("channel")) {
    return RPC_ERROR_INVALID_PARAMS;
  }

  uint8_t channel = params["channel"];

  if (channel > QC_MAX_CHANNEL) {
    return RPC_ERROR_INVALID_PARAMS;
  }

  qc.disableCounter(channel);
  return RPC_OK;
}

int RpcServer::rpc_qcClearCountRegister(JsonObject params) {
  if (!params.containsKey("channel")) {
    return RPC_ERROR_INVALID_PARAMS;
  }

  uint8_t channel = params["channel"];

  if (channel > QC_MAX_CHANNEL) {
    return RPC_ERROR_INVALID_PARAMS;
  }

  qc.clearCountRegister(channel);
  return RPC_OK;
}

int RpcServer::rpc_qcReadCountRegister(JsonObject params) {
  if (!params.containsKey("channel")) {
    return RPC_ERROR_INVALID_PARAMS;
  }

  uint8_t channel = params["channel"];

  if (channel > QC_MAX_CHANNEL) {
    return RPC_ERROR_INVALID_PARAMS;
  }

  int32_t count = qc.readCountRegister(channel);
  response_data["count"] = count;
  return RPC_OK;
}
#endif

// OLED RPC functions (must be outside of any function body)
#if defined INCLUDE_OLED_DISPLAY
int RpcServer::rpc_oledClear(JsonObject params) {
  oled_Display.Clear();
  return RPC_OK;
}

int RpcServer::rpc_oledWriteLine(JsonObject params) {
  if (!params.containsKey("line") || !params.containsKey("text") || !params.containsKey("align")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  uint8_t line = params["line"];
  const char* text = params["text"];
  uint8_t align = params["align"];
  oled_Display.WriteLine(line, text, align);
  return RPC_OK;
}
#endif

#if defined INCLUDE_DAC_4922_LIB
// DAC RPC functions
int RpcServer::rpc_dacSetVoltage(JsonObject params) {
  if (!params.containsKey("channel") || !params.containsKey("voltage")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  uint8_t channel = params["channel"];
  float voltage = params["voltage"];
  dac.SetOutputVoltage(channel, voltage);
  return RPC_OK;
}

int RpcServer::rpc_dacSetVoltageAll(JsonObject params) {
  if (!params.containsKey("voltage")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  float voltage = params["voltage"];
  dac.SetOutputVoltageAll(voltage);
  return RPC_OK;
}
#endif

// ADC RPC functions
int RpcServer::rpc_adcReadRaw(JsonObject params) {
  if (!params.containsKey("channel")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t channel = params["channel"];
  uint8_t averageCount = params.containsKey("averageCount") ? params["averageCount"] : 1;
  
#if defined INCLUDE_ADC_3208_LIB
  uint16_t raw_value = adc.ReadRaw(channel, averageCount);
  response_data["raw"] = raw_value;
#else
  response_data["raw"] = 0;
#endif
  
  return RPC_OK;
}

int RpcServer::rpc_adcReadVoltage(JsonObject params) {
  if (!params.containsKey("channel")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t channel = params["channel"];
  uint8_t averageCount = params.containsKey("averageCount") ? params["averageCount"] : 1;
  
#if defined INCLUDE_ADC_3208_LIB
  double voltage = adc.ReadVoltage(channel, averageCount);
  response_data["voltage"] = voltage;
#else
  response_data["voltage"] = 0.0;
#endif
  
  return RPC_OK;
}

int RpcServer::rpc_isButtonPressed(JsonObject params) {
  if (!params.containsKey("analogButton")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t analogButton = params["analogButton"];
  
#if defined INCLUDE_ADC_3208_LIB
  bool pressed = adc.IsButtonPressed(analogButton);
  response_data["pressed"] = pressed;
#else
  response_data["pressed"] = false;
#endif
  
  return RPC_OK;
}

#if defined INCLUDE_DIO_LIB
// DIO RPC functions
int RpcServer::rpc_dioGetInput(JsonObject params) {
  uint8_t input_value = digital_io.GetInput();
  response_data["value"] = input_value;
  return RPC_OK;
}

int RpcServer::rpc_dioIsBitSet(JsonObject params) {
  if (!params.containsKey("bitNumber")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t bitNumber = params["bitNumber"];
  bool bitSet = digital_io.IsBitSet(bitNumber);
  response_data["bitSet"] = bitSet;
  return RPC_OK;
}

int RpcServer::rpc_dioSetOutput(JsonObject params) {
  if (!params.containsKey("value")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t value = params["value"];
  digital_io.SetOutput(value);
  return RPC_OK;
}

int RpcServer::rpc_dioSetBit(JsonObject params) {
  if (!params.containsKey("bitNumber")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t bitNumber = params["bitNumber"];
  digital_io.SetBit(bitNumber);
  return RPC_OK;
}

int RpcServer::rpc_dioClearBit(JsonObject params) {
  if (!params.containsKey("bitNumber")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t bitNumber = params["bitNumber"];
  digital_io.ClearBit(bitNumber);
  return RPC_OK;
}

int RpcServer::rpc_dioToggleBit(JsonObject params) {
  if (!params.containsKey("bitNumber")) {
    return RPC_ERROR_INVALID_PARAMS;
  }
  
  uint8_t bitNumber = params["bitNumber"];
  digital_io.ToggleBit(bitNumber);
  return RPC_OK;
}

#endif