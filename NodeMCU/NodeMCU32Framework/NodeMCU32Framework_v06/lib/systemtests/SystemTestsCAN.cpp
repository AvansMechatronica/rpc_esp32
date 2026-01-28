//////////////////////////////////////////////////////////////////////////////
//
// SystemTestsCAN.cpp
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
#include "MCP2515v01.h"
#include "SerialPrintf.h"
#include "Config.h"
#include "SystemTests.h"
#include "SystemTestsCAN.h"

///////////////////////////////////////////////////////////////////////////////
// external objects in another file

extern MCP2515 canDevice;

///////////////////////////////////////////////////////////////////////////////
// uint8_t test_can_SetupForTest(bool internalLoopback)

uint8_t test_can_SetupForTest(bool internalLoopback)
{
	uint8_t errorCount = 0;
	MCP2515::ERROR error = MCP2515::ERROR_OK;

	error = canDevice.reset();
	if (error != MCP2515::ERROR_OK)
	{
		canDevice.printCANError(error);
		errorCount++;
	}

	error = canDevice.setBitrate(CAN_500KBPS, MCP_16MHZ);
	if (error != MCP2515::ERROR_OK)
	{
		canDevice.printCANError(error);
		errorCount++;
	}
	
	if (internalLoopback)
	{
		error = canDevice.setLoopbackMode();
	}
	else	// echo mode with external CAN device
	{
		error = canDevice.setNormalMode();
	}

	if (error != MCP2515::ERROR_OK)
	{
		canDevice.printCANError(error);
		errorCount++;
	}

	return errorCount;
}

///////////////////////////////////////////////////////////////////////////////
// uint32_t test_can_Loopback(bool internalLoopback)
//
// device must be in loopback mode for INTERNAL loopback!! External loopback
// requires an external device to echo the message onto the CAN bus

uint32_t test_can_Loopback(bool internalLoopback)
{
	uint32_t errorCount = 0;
	uint8_t ix = 0;
	MCP2515::ERROR error = MCP2515::ERROR_OK;

	static uint8_t testData = 0;	// must be static!

	can_frame canFrameTx;	// CAN transmit buffer
	can_frame canFrameRc;	// CAN receive buffer

	memset(canFrameTx.data, 0x00, CAN_MAX_DLEN);
	memset(canFrameRc.data, 0x00, CAN_MAX_DLEN);

	canFrameTx.can_id  = (testData % 0x7ff);	// 11 bits max for standard CAN id
	canFrameTx.can_dlc = CAN_MAX_DLEN;			// maximum message length of 8 bytes
	for (ix = 0; ix < CAN_MAX_DLEN; ix++)
	{
		canFrameTx.data[ix] = testData + ix;
	}

	error = canDevice.sendMessage(&canFrameTx);
	if (error != MCP2515::ERROR_OK)
	{
		canDevice.printCANError(error);
		errorCount++;
	}

	uint32_t sleepTimeMs = 1;
	uint16_t waitcount   = 0;

	// wait until the external device echoes the message transmitted:

	while ( (canDevice.checkReceive() == false) && (waitcount < 100) )
	{
		taskSleep(sleepTimeMs);
		waitcount++;
	}

	if (canDevice.checkReceive() == true)
	{
		// SerialPrintf("> CAN echo message received! (wait time = %d ms)\n", waitcount*sleepTimeMs);
	}
	else
	{ 
		SerialPrintf("> CAN %s receive timeout\n", internalLoopback ? "loopback" : "echo");
	}

	error = canDevice.readMessage(&canFrameRc);
	if (error != MCP2515::ERROR_OK)
	{
		canDevice.printCANError(error);
		errorCount++;
	}

	if (canFrameTx.can_id != canFrameRc.can_id)
	{
		SerialPrintf("> CAN id error: tx = 0x%08x, rc = 0x%08x\n",
					 canFrameTx.can_id, canFrameRc.can_id);
		errorCount++;
	}
	
	if (canFrameTx.can_dlc != canFrameRc.can_dlc)
	{
		SerialPrintf("> CAN dlc error: tx = %d, rc = %d\n",
					 canFrameTx.can_dlc, canFrameRc.can_dlc);
		errorCount++;
	}

	for (ix = 0; ix < CAN_MAX_DLEN; ix++)
	{
		if (canFrameRc.data[ix] != canFrameTx.data[ix])
		{
			SerialPrintf("> CAN data error: tx[%d] = %d, rc[%d] = %d\n",
						 ix, canFrameTx.data[ix], ix, canFrameRc.data[ix]);
			errorCount++;
		}
	}
 
	testData++;

	return errorCount;
}

///////////////////////////////////////////////////////////////////////////////
// void test_can_Loopback_Repeat(bool internalLoopback)

void test_can_Loopback_Repeat(bool internalLoopback)
{
	uint32_t errorCount = 0;
	uint32_t pass = 0;
	char msg[40];
	
	sprintf(msg, "CAN %s test", internalLoopback ? "loopback" : "echo");

	errorCount += test_can_SetupForTest(internalLoopback);

	while (true)
	{
		errorCount += test_can_Loopback(internalLoopback);

		test_ShowPass(++pass, 100);
		test_ErrorReport(msg, pass, errorCount, 1000);

		if (StopTest()) break;
	}
}
