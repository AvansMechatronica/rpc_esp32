///////////////////////////////////////////////////////////////////////////////
//
// NodeMCUFramework_v06.cpp
//
// Authors: 	Roel Smeets
// Edit date: 	02-06-2025
//				10-08-2025
//				14-11-2025
//				13-12-2025
//
///////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////
// system #includes

#include <Arduino.h>
#include "esp_timer.h"
#include "esp_system.h"
#include "esp_log.h"
#include "esp_task_wdt.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/uart.h"
#include "WiFi.h"

///////////////////////////////////////////////////////////////////////////////
// application #includes

#include "SerialPrintf.h"
#include "TaskSleep.h"
#include "TaskHeartbeat.h"
#include "Config.h"
#include "TaskCLIHandler.h"
#include "TaskCommandHandler.h"
#include "InfoRTOS.h"
#include "IOLib.h"
#include "ExtIOLib.h"
#include "InterruptLib.h"
#include "LEDLib.h"
#include "ButtonLib.h"
#include "SPILib.h"
#include "I2CLib.h"
#include "OLEDLibESP32.h"
#include "I2CScanner.h"
#include "QC7366Lib.h"
#include "UART740Lib.h"
#include "SystemTests.h"
#include "DAC4922Lib.h"
#include "SPIeeprom.h"
#include "MCP2515v01.h"

///////////////////////////////////////////////////////////////////////////////
// Global CAN object

#if (I2CSPI_BRIDGE_USED == 1)
MCP2515 canDevice(I2C_ADDRESS_SPIBRIDGE, SPI_CAN_SLAVEADDRESS);
#else
MCP2515 canDevice(SPI_DEVICE_CAN);
#endif

///////////////////////////////////////////////////////////////////////////////
// Global declarations, task handles

xTaskHandle handle_HartbeatTask	= NULL;
xTaskHandle handle_CLITask		= NULL;
xTaskHandle handle_CmdTask		= NULL;

///////////////////////////////////////////////////////////////////////////////
// wrapper, simplified version of xTaskCreatePinnedToCore

bool platformTaskCreate(TaskFunction_t taskCode, const char * const taskName, 
                        TaskHandle_t * const taskHandle)
{
    BaseType_t taskResult = pdFAIL;
    bool taskOK = false;
  
    taskResult = xTaskCreatePinnedToCore(taskCode, taskName, 
                RTOS_DEFAULT_STACKSIZE, NULL, 1, taskHandle, CORE_1);
    
    info_RegisterTaskByName(taskName);

    taskOK = (taskResult == pdPASS);
    SerialPrintf("> task [%s] creation %s\n", taskName, taskOK ? "OK" : "FAILED");

    return taskOK;
}

///////////////////////////////////////////////////////////////////////////////
// bool platformInit(void)

#include <Wire.h>

bool platformInit(void)
{
    bool i2cOK   = false;
    bool oledOK  = false;
    bool uartOK  = false;
    bool result  = true;

    uint8_t nDevices = 0;

	io_Init();
    led_Init();
    button_Init();
    spi_Init();
    qc_Init();
	dac_Init();

    i2cOK   = i2c_Init();
    oledOK  = oled_Init();
    uartOK  = uart_Init();

    SerialPrintf("> I2C  init %s\n", i2cOK  ? "OK" : "*** FAILED ***");
    SerialPrintf("> OLED init %s\n", oledOK ? "OK" : "*** FAILED ***");
    SerialPrintf("> UART init %s\n", uartOK ? "OK" : "*** FAILED ***");

	result = i2cOK && oledOK && uartOK;

    nDevices = i2c_ScanBus();
	SerialPrintf("> I2C devices found: %d\n", nDevices);

	bool extIOPresent = i2c_ProbeAddress(I2C_ADDRESS_EXT_IN) && i2c_ProbeAddress(I2C_ADDRESS_EXT_OUT);
	if (extIOPresent)
	{
		bool extioOK = extio_Init();
		SerialPrintf("> EXTIO init %s\n", extioOK ? "OK" : "*** FAILED ***");
	}
	else
	{
		SerialPrintf("> External I2C IO device not present\n");
	}

	bool i2cspiBridgePresent = i2c_ProbeAddress(I2C_ADDRESS_SPIBRIDGE);
	if (i2cspiBridgePresent)
	{
		MCP2515::ERROR canResult = canDevice.begin();
		canDevice.printCANError(canResult);
		SerialPrintf("> CAN init %s\n", (canResult == MCP2515::ERROR_OK) ? "OK" : "*** FAILED ***");
	}
	else
	{
		SerialPrintf("> External I2C/SPI bridge device not present\n");
	}

    SerialPrintf("> DAC resolution = %10.6f Volt\n", DAC_RESOLUTION);
    SerialPrintf("> DAC min        = %10.6f Volt\n", DAC_MIN_VOLTAGE);
    SerialPrintf("> DAC max        = %10.6f Volt\n", DAC_MAX_VOLTAGE);

    cliMessageQueue = xQueueCreate(QUEUESIZE, sizeof(CLI_MESSAGE));

    result &= platformTaskCreate(task_Heartbeat,      "task_heartbeat", &handle_HartbeatTask);
    result &= platformTaskCreate(task_CLIHandler,     "task_cli",       &handle_CLITask);
    result &= platformTaskCreate(task_CommandHandler, "task_cmd",       &handle_CmdTask);

    // manually register default system tasks:
    info_RegisterTaskByName("main");
    info_RegisterTaskByName("esp_timer");
    info_RegisterTaskByName("IDLE0");
    info_RegisterTaskByName("IDLE1");
    info_RegisterTaskByName("Tmr Svc");
    info_RegisterTaskByName("ipc0");
    info_RegisterTaskByName("ipc1");
    info_RegisterTaskByName("loopTask");

    return result;
}

///////////////////////////////////////////////////////////////////////////////
// void setup()

void setup()
{
    bool result = false;

	Serial.begin(115200);
	SerialPrintf("> NodeMCUFramework_v06\n");
	SerialPrintf("> build: %s\n", __TIMESTAMP__);
	SerialPrintf("> running setup\n");

    result = platformInit();

   	SerialPrintf("> setup done: %s\n", (result == true) ? "OK" : "FAILED");

	oled_Clear();
	oled_WriteLine(0, "NodeMCU32S", ALIGN_CENTER);
	oled_WriteLine(1, "Framework",  ALIGN_CENTER);
	oled_WriteLine(2, "V0.6",  		ALIGN_CENTER);

    // TODO: add user tasks here:

    // xTaskCreatePinnedToCore( userTaskFunction, "task_name", 
    //                          RTOS_DEFAULT_STACKSIZE, NULL, priority, &handle_UserTaskfunction, 
    //                          CORE_1);
    // info_RegisterTaskByName("task_name");

	info_Tasks();

    #if (SYSTEMTEST_ONLY == 1)
	SerialPrintf("> running system tests...\n");
	// RunSystemTests();	// for separate HW testing
	RunSystemTestsMenu();	// via user menu
	#endif
}


///////////////////////////////////////////////////////////////////////////////
// void loop()

void loop()
{
	static uint32_t loopcount = 0;

	SerialPrintf("> looping %ld...\n", loopcount);
    taskSleep(500);
	loopcount++;
}
