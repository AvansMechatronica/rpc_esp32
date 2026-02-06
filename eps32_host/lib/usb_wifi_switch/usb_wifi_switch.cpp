#include "usb_wifi_switch.h"


#if defined (INCLUDE_OLED_DISPLAY)
#include "oled_lib.h"
extern oledDisplay  oled_Display;
#endif





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


bool check_wifi_mode(){
    bool result = false;
    result = LittleFS.begin(true);

    if (!result) {
        DEBUG_PRINT("No file system found assuming USB mode\n");
        return false;
    }
 
    String mode = readFile(LittleFS, "/comm_mode.txt");
    if(mode == "WIFI"){
        DEBUG_PRINT("WiFi mode detected\n");
        result = true;
    }
    else{
        DEBUG_PRINT("USB mode detected\n");
        result = false;
    }
    LittleFS.end();
    return result;

}


void toggle_usb_wifi_mode(){
    bool result = false;
    result = LittleFS.begin(true);

    if (!result) {
        DEBUG_PRINT("No file system install with platformIO\n");
#if defined (INCLUDE_OLED_DISPLAY)
        oled_Display.clear();
        oled_Display.writeLine(0, "No filesystem", ALIGN_CENTER);
        oled_Display.writeLine(1, "found",  ALIGN_CENTER);
        oled_Display.writeLine(2, "Install",  		ALIGN_CENTER);
        oled_Display.writeLine(3, "Through PlatformIO",  		ALIGN_CENTER);
        delay(2000);
#endif
    }
    String mode = readFile(LittleFS, "/comm_mode.txt");
    if(mode == "WIFI"){
        DEBUG_PRINT("Switching to USB mode\n");
        writeFile(LittleFS, "/comm_mode.txt", "USB");
#if defined (INCLUDE_OLED_DISPLAY)
        oled_Display.clear();
        oled_Display.writeLine(0, "Communication", ALIGN_CENTER);
        oled_Display.writeLine(1, "mode",  ALIGN_CENTER);
        oled_Display.writeLine(2, "changed to",  ALIGN_CENTER);
        oled_Display.writeLine(3, "USB",  		ALIGN_CENTER);
        delay(2000);
#endif    
    }
    else{
        DEBUG_PRINT("Switching to WiFi mode\n");
        writeFile(LittleFS, "/comm_mode.txt", "WIFI");
#if defined (INCLUDE_OLED_DISPLAY)
        oled_Display.clear();
        oled_Display.writeLine(0, "Communication", ALIGN_CENTER);
        oled_Display.writeLine(1, "mode",  ALIGN_CENTER);
        oled_Display.writeLine(2, "changed to",  ALIGN_CENTER);
        oled_Display.writeLine(3, "WIFI",  		ALIGN_CENTER);
        delay(2000);
#endif    
    }
    LittleFS.end(); 
}