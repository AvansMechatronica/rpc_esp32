//////////////////////////////////////////////////////////////////////////////
//
// SystemTestsExtIO.cpp
//
// Authors: 	Roel Smeets
// Edit date: 	13-12-2025
//
///////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////
// system #includes

#include <Arduino.h>

///////////////////////////////////////////////////////////////////////////////
// application #includes

#include "TaskSleep.h"
#include "ExtIOLib.h"
#include "SerialPrintf.h"
#include "Config.h"
#include "SystemTests.h"
#include "SystemTestsExtIO.h"


///////////////////////////////////////////////////////////////////////////////
// uint8_t test_extio_RW(uint8_t write)

uint8_t test_extio_RW(uint8_t write)
{
	uint8_t read  = 0;
	uint8_t error = 0;

	write = write & 0xff;

	extio_SetOutput(write);
	read = extio_GetInput();
	// taskSleep(500);
	if (read != write)
	{
		SerialPrintf("> External I/O R/W error: write = 0x%02x, read = 0x%02x\n", write, read);
		error++;
	}
	
	return error;
}

///////////////////////////////////////////////////////////////////////////////
// uint32_t test_extio_Loopback(void)

uint32_t test_extio_Loopback(void)
{
	uint16_t write = 0;
	uint16_t maxValue = 0xff;
	uint16_t errorCount = 0;
	uint8_t  ix = 0;

	// 1: increment
	for (write = 0; write <= maxValue; write++)
	{
		errorCount += test_extio_RW(write);
	}

	// 2: walking 1
	for (ix = 0 ; ix < N_EXT_OUTPUT_BITS; ix++)
	{
		write = 0x01 << ix;
		errorCount += test_extio_RW(write);
	}
	
	// 3: walking 0
	for (ix = 0 ; ix < N_EXT_OUTPUT_BITS; ix++)
	{
		write = ~(0x01 << ix);
		errorCount += test_extio_RW(write);
	}

	// 4: flipping bits
	errorCount += test_extio_RW(0x00);
	errorCount += test_extio_RW(0xff);
	errorCount += test_extio_RW(0xaa);
	errorCount += test_extio_RW(0x55);

	return errorCount;
}

///////////////////////////////////////////////////////////////////////////////
// void test_extio_Loopback_Repeat(void)

void test_extio_Loopback_Repeat(void)
{
	uint32_t errorCount = 0;
	uint32_t pass = 0;

	while (true)
	{
		errorCount += test_extio_Loopback();

		test_ShowPass(++pass, 1);
		test_ErrorReport("External I/O loopback test", pass, errorCount, 10);

		if (StopTest()) break;
	}
}
