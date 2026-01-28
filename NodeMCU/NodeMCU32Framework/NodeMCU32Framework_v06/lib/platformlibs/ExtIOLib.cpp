///////////////////////////////////////////////////////////////////////////////
//
// ExtIOLib.cpp
//
// Authors: 	Roel Smeets
// Edit date: 	02-06-2025
//
///////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////
// system #includes

#include <Arduino.h>
#include <Wire.h>

///////////////////////////////////////////////////////////////////////////////
// application #includes

#include "I2CLib.h"
#include "ExtIOLib.h"
#include "Config.h"
#include "SerialPrintf.h"

///////////////////////////////////////////////////////////////////////////////
// file globals, reflects availability of I2C input port & output port

static bool g_InputConnected  = false;
static bool g_Outputconnected = false;

///////////////////////////////////////////////////////////////////////////////
// bool extio_IsInputConnected(void)

bool extio_IsInputConnected(void)
{
	uint8_t result = 0;

	Wire.beginTransmission(I2C_ADDRESS_EXT_IN);
	result = Wire.endTransmission();

	return (result == 0);
}

///////////////////////////////////////////////////////////////////////////////
// bool extio_IsOutputConnected(void)

bool extio_IsOutputConnected(void)
{
	uint8_t result = 0;

	Wire.beginTransmission(I2C_ADDRESS_EXT_OUT);
	result = Wire.endTransmission();

	return (result == 0);
}

///////////////////////////////////////////////////////////////////////////////
// bool extio_Init(void)

bool extio_Init(void)
{
	uint8_t result  = 0;

	// I2C output register
	g_Outputconnected = extio_IsOutputConnected();
	if (g_Outputconnected)
	{
		extio_SetOutput(0x00);
	}

	// I2C input register
	g_InputConnected = extio_IsInputConnected();

	return (g_InputConnected && g_Outputconnected);
}

///////////////////////////////////////////////////////////////////////////////
// void extio_SetOutput(uint8_t value)

bool extio_SetOutput(uint8_t value)
{
	bool result = false;

	if (g_Outputconnected)
	{
		Wire.beginTransmission(I2C_ADDRESS_EXT_OUT);
		Wire.write(value);
		Wire.endTransmission();

		result = true;
	}

	return result;
}

///////////////////////////////////////////////////////////////////////////////
// uint8_t extio_GetInput(void)

uint8_t extio_GetInput(void)
{
	uint8_t value = 0;

    bool sendStop = false;
    uint16_t nrOfBytes = 1;

	if (g_InputConnected)
	{
	    Wire.requestFrom(I2C_ADDRESS_EXT_IN, nrOfBytes, (int)(sendStop = true));
		value = Wire.read();
	}
	
	return value;
}

///////////////////////////////////////////////////////////////////////////////
// bool extio_IsValidBitNumber(uint8_t bitNumber)

bool extio_IsValidBitNumber(uint8_t bitNumber)
{
	bool isValid = false;

	isValid = (bitNumber < N_EXT_INPUT_BITS);

	return isValid;
}

///////////////////////////////////////////////////////////////////////////////
// bool extio_IsBitSet(uint8_t bitNumber)

bool extio_IsBitSet(uint8_t bitNumber)
{
	bool isBitSet = false;
	uint8_t data = 0;
	uint8_t mask = _BV(bitNumber);

	if (extio_IsValidBitNumber(bitNumber))
	{
		data = extio_GetInput();
		isBitSet = ((data & mask) != 0);
	}
	
	return isBitSet;
}


///////////////////////////////////////////////////////////////////////////////
// void extio_SetBit(uint8_t bitNumber, bool bitOn)

void extio_SetBit(uint8_t bitNumber, bool bitOn)
{
	uint8_t data = 0;
	uint8_t mask = _BV(bitNumber);

	if (extio_IsValidBitNumber(bitNumber))
	{
		data = extio_GetInput();
		if (bitOn)
		{
			data = data | mask;
		}
		else
		{
			data = data & ~mask;
		}
		extio_SetOutput(data);
	}
}


