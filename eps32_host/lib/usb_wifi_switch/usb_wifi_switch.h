#ifndef LIB_USB_WIFI_SWITCH_USB_WIFI_SWITCH_H_
#define LIB_USB_WIFI_SWITCH_USB_WIFI_SWITCH_H_

#include <Arduino.h>
#include "LittleFS.h"

extern String readFile(fs::FS &fs, const char * path);
extern void writeFile(fs::FS &fs, const char * path, const char * message);

bool check_wifi_mode();
void toggle_usb_wifi_mode();


#endif