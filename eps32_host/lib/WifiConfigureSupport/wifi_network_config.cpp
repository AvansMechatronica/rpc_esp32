#ifdef WIFI_CONFIGURE_SERVER
#include <Arduino.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include <ESPAsyncWebServer.h>
#include <AsyncTCP.h>

// Include appropriate filesystem
#ifdef USE_SPIFFS
  #include "SPIFFS.h"
  #define FS_SYSTEM SPIFFS
  #define FS_NAME "SPIFFS"
#else
  #include "LittleFS.h"
  #define FS_SYSTEM LittleFS
  #define FS_NAME "LittleFS"
#endif

#include "wifi_network_config.h"
#if defined (INCLUDE_OLED_DISPLAY)
#include "oled_lib.h"
extern oledDisplay  oled_Display;
#endif

#include <string>

#define DEBUG
#ifdef DEBUG
#define DEBUG_PRINT(fmt, ...) \
    do { \
        Serial.printf("DEBUG: %s:%d:%s(): " fmt, \
                __FILE__, __LINE__, __func__, ##__VA_ARGS__); \
    } while (0)
#else
#define DEBUG_PRINT(fmt, ...) \
    do {} while (0)
#endif

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

// Search for parameter in HTTP POST request
const char* PARAM_INPUT_1 = "ssid";
const char* PARAM_INPUT_2 = "pass";


// Variables to save values from HTML form
String ssid;
String pass;


// File paths to save input values permanently
const char* ssidPath = "/ssid.txt";
const char* passPath = "/pass.txt";



// Timer variables
unsigned long previousMillis = 0;
const long interval = 10000;  // interval to wait for Wi-Fi connection (milliseconds)

// Initialize filesystem (LittleFS or SPIFFS)
void initFS() {
  bool result;
  
#ifdef USE_SPIFFS
  result = SPIFFS.begin(false);
#else
  result = LittleFS.begin(true);
#endif

  if (!result) {
    DEBUG_PRINT("An error has occurred while mounting %s\n", FS_NAME);
#if defined (INCLUDE_OLED_DISPLAY)
    oled_Display.Clear();
    oled_Display.WriteLine(0, "No filesystem", ALIGN_CENTER);
    oled_Display.WriteLine(1, "detected",  ALIGN_CENTER);
    oled_Display.WriteLine(2, "Install by",  		ALIGN_CENTER);
    oled_Display.WriteLine(3, "PlatformIO",  		ALIGN_CENTER);
#endif
    while(true){};
  }
  DEBUG_PRINT("%s mounted successfully\n", FS_NAME);
}

// Read File from filesystem
String readFile(fs::FS &fs, const char * path){
  DEBUG_PRINT("Reading file: %s\r\n", path);

  File file = fs.open(path);
  if(!file || file.isDirectory()){
    DEBUG_PRINT("- failed to open file for reading\n");
    return String();
  }
  
  String fileContent;
  while(file.available()){
    fileContent = file.readStringUntil('\n');
    break;     
  }
  file.close();
  DEBUG_PRINT("- read from file: %s\n", fileContent.c_str());
  return fileContent;
}

// Write file to filesystem
void writeFile(fs::FS &fs, const char * path, const char * message){
  DEBUG_PRINT("Writing file: %s\r\n", path);

  File file = fs.open(path, FILE_WRITE);
  if(!file){
    DEBUG_PRINT("- failed to open file for writing\n");
    return;
  }
  if(file.print(message)){
    DEBUG_PRINT("- file written\n");
  } else {
    DEBUG_PRINT("- write failed\n");
  }
  file.close();
}

// Initialize WiFi
bool testWifi() {
  if(ssid=="" || pass==""){
    DEBUG_PRINT("Undefined SSID or Password\n");
    return false;
  }

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid.c_str(), pass.c_str());
  DEBUG_PRINT("Connecting to WiFi...\n");
#if defined (INCLUDE_OLED_DISPLAY)
  oled_Display.Clear();
  oled_Display.WriteLine(0, "Connecting", ALIGN_CENTER);
  oled_Display.WriteLine(1, "to WiFi...",  ALIGN_CENTER);
#endif

  unsigned long currentMillis = millis();
  previousMillis = currentMillis;

  while(WiFi.status() != WL_CONNECTED) {
    currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
      DEBUG_PRINT("Failed to connect\n");
#if defined (INCLUDE_OLED_DISPLAY)
    oled_Display.Clear();
    oled_Display.WriteLine(0, "Failed to", ALIGN_CENTER);
    oled_Display.WriteLine(1, "connect to",  ALIGN_CENTER);
    oled_Display.WriteLine(2, "WiFi",  		ALIGN_CENTER);

#endif
      return false;
    }
  }

  DEBUG_PRINT("Connected to WiFi\n");
  DEBUG_PRINT("IP Address: %s\n", WiFi.localIP().toString().c_str());
  return true;
}

NETWORK_CONFIG network_config;

// Handle POST request for WiFi configuration
void handleConfigPost(AsyncWebServerRequest *request) {
  int params = request->params();
  for(int i=0; i<params; i++){
    const AsyncWebParameter* p = request->getParam(i);
    if(p->isPost()){
      // HTTP POST ssid value
      if (p->name() == PARAM_INPUT_1) {
        ssid = p->value().c_str();
        DEBUG_PRINT("SSID set to: %s\n", ssid.c_str());
        // Write file to save value
        writeFile(FS_SYSTEM, ssidPath, ssid.c_str());
      }
      // HTTP POST pass value
      if (p->name() == PARAM_INPUT_2) {
        pass = p->value().c_str();
        DEBUG_PRINT("Password set to: %s\n", pass.c_str());
        // Write file to save value
        writeFile(FS_SYSTEM, passPath, pass.c_str());
      }
    }
  }
  request->send(200, "text/plain", "Done. Controller will restart");
#if defined (INCLUDE_OLED_DISPLAY)
  oled_Display.Clear();
  oled_Display.WriteLine(0, "WiFi", ALIGN_CENTER);
  oled_Display.WriteLine(1, "configuration",  ALIGN_CENTER);
  oled_Display.WriteLine(2, "stored",  		ALIGN_CENTER);
  oled_Display.WriteLine(3, "Restarting...",  ALIGN_CENTER);
#endif
  delay(3000);
  ESP.restart();
}

// Returns true if the network was configured and WiFi connection succeeded (station mode).
// Returns false if the device entered AP mode for configuration or if configuration is incomplete.
bool configureNetwork(bool forceConfigure, NETWORK_CONFIG *networkConfig) {

  initFS();

  // Detect webserver files
  File file = FS_SYSTEM.open("/wifimanager.html");
  if(!file){
    DEBUG_PRINT("No webpages file found\n");
#if defined (INCLUDE_OLED_DISPLAY)
    oled_Display.Clear();
    oled_Display.WriteLine(0, "No webpages", ALIGN_CENTER);
    oled_Display.WriteLine(1, "found",  ALIGN_CENTER);
    oled_Display.WriteLine(2, "Install by",  		ALIGN_CENTER);
    oled_Display.WriteLine(3, "PlatformIO",  		ALIGN_CENTER);
#endif
    while(true){};
  }
  file.close();
 
  // Load values saved in filesystem
  ssid = readFile(FS_SYSTEM, ssidPath);
  pass = readFile(FS_SYSTEM, passPath);


  DEBUG_PRINT("ssid : %s\n", ssid.c_str());
  DEBUG_PRINT("pass : %s\n", pass.c_str());


  if(testWifi() && !forceConfigure) {
    networkConfig->password = pass;
    networkConfig->ssid = ssid;
    return true;
  }
  else {
    // Bring up AP and keep STA enabled for scanning
    WiFi.mode(WIFI_AP_STA);
    const char *ap_name = "Esp32Remote";
    DEBUG_PRINT("Setting AP (Access Point)\n");

    // NULL sets an open Access Point
    WiFi.softAP(ap_name, NULL);

    IPAddress IP = WiFi.softAPIP();
    DEBUG_PRINT("AP IP address: %s\n", IP.toString().c_str());

#if defined (INCLUDE_OLED_DISPLAY)
    char text_buffer[32];
    oled_Display.Clear();
    oled_Display.WriteLine(0, "Connect to AP:", ALIGN_CENTER);
    snprintf(text_buffer, sizeof(text_buffer), "%s", ap_name);
    oled_Display.WriteLine(1, text_buffer,  ALIGN_CENTER);
    snprintf(text_buffer, sizeof(text_buffer), "IP: %s", IP.toString().c_str());
    oled_Display.WriteLine(2, text_buffer,  ALIGN_CENTER);
#endif

    // Web Server Root URL - serve static files first
    server.serveStatic("/style.css", FS_SYSTEM, "/style.css");
    

    server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
      request->send(FS_SYSTEM, "/wifimanager.html", "text/html");
    });
    
    // WiFi scan endpoint -> returns JSON list of networks
    server.on("/scan", HTTP_GET, [](AsyncWebServerRequest *request){
      // Ensure STA interface is enabled for scanning
      WiFi.mode(WIFI_AP_STA);
      int n = WiFi.scanNetworks();
      DynamicJsonDocument doc(2048);
      JsonArray arr = doc.createNestedArray("networks");
      for (int i = 0; i < n; i++) {
        JsonObject o = arr.createNestedObject();
        o["ssid"] = WiFi.SSID(i);
        o["rssi"] = WiFi.RSSI(i);
        o["enc"] = (int)WiFi.encryptionType(i);
        o["bssid"] = WiFi.BSSIDstr(i);
        o["channel"] = WiFi.channel(i);
      }
      String out;
      serializeJson(doc, out);
      request->send(200, "application/json", out);
    });
    
#if 1
    server.on("/", HTTP_POST, [](AsyncWebServerRequest *request) {
      handleConfigPost(request);
    });
#endif 
    // Handle not found
    //server.onNotFound([](AsyncWebServerRequest *request){
    //  request->send(404, "text/plain", "Not found");
    //});
    
    server.begin();
    DEBUG_PRINT("Web server started\n");
    pinMode(LED_BUILTIN, OUTPUT);
    // Flash the built-in LED while in AP mode
    while(true){
      // Stay in AP mode until configured
      digitalWrite(LED_BUILTIN, HIGH);
      vTaskDelay(250 / portTICK_PERIOD_MS);
      digitalWrite(LED_BUILTIN, LOW);
      vTaskDelay(250 / portTICK_PERIOD_MS);
    }
    return false;
  }
}
#endif //WIFI