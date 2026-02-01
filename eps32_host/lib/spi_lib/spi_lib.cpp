///////////////////////////////////////////////////////////////////////////////
//
// SPILib.cpp
//
// Authors: 	Roel Smeets
// Edit date: 	02-06-2025
//
///////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////
// system #includes

#include <Arduino.h>
#include <spi.h>

///////////////////////////////////////////////////////////////////////////////
// application #includes

#include "spi_lib.h"


///////////////////////////////////////////////////////////////////////////////
// void spi_Init(void)

void spi::Init(void)
{
	if (g_IsSPIInitialised == false)	// prevents multiple inits
	{
		pinMode(SPI_SEL_2, OUTPUT);
		pinMode(SPI_SEL_1, OUTPUT);
		pinMode(SPI_SEL_0, OUTPUT);

        // deselects all SPI devices:
        DeselectDevice();

        // same as in constructor
        Settings._clock    = SPI_DEFAULT_SPEED;
        Settings._bitOrder = MSBFIRST;
        Settings._dataMode = SPI_MODE0;

		vspi.begin(VSPI_SCLK, VSPI_MISO, VSPI_MOSI, VSPI_SS);
		vspi.setHwCs(false);  // false = disable VSPI_SS, Default = disabled!

		g_IsSPIInitialised = true;
	}
}

///////////////////////////////////////////////////////////////////////////////
// void spi::BeginTransaction(SPISettings settings)

void spi::BeginTransaction(SPISettings settings)
{
    vspi.beginTransaction(settings);
}

///////////////////////////////////////////////////////////////////////////////
// void spi::EndTransaction(void)

void spi::EndTransaction(void)
{
    vspi.endTransaction();
}

///////////////////////////////////////////////////////////////////////////////
// void spi::WriteByte(const uint8_t data)

void spi::WriteByte(const uint8_t data)
{
	vspi.write(data);
}

///////////////////////////////////////////////////////////////////////////////
// void spi::WriteWord(const uint16_t data)

void spi::WriteWord(const uint16_t data)
{
	vspi.write16(data);
}

///////////////////////////////////////////////////////////////////////////////
// void spi::ReadByte(uint8_t *byteData)

void spi::ReadByte(uint8_t *byteData)
{
	*byteData = vspi.transfer(0);
}

///////////////////////////////////////////////////////////////////////////////
// void spi::ReadWord(uint16_t *wordData)

void spi::ReadWord(uint8_t *wordData)
{
	*wordData = vspi.transfer16(0);
}


///////////////////////////////////////////////////////////////////////////////
// uint8_t spi::TransferByte(uint8_t byteToSend)

uint8_t spi::TransferByte(uint8_t byteToSend)
{
	uint8_t rcvByte = vspi.transfer(byteToSend);
 
	return rcvByte;
}

///////////////////////////////////////////////////////////////////////////////
// uint16_t spi::TransferByte(uint8_t byteToSend)

uint16_t spi::TransferWord(uint16_t wordToSend)
{
	uint16_t rcvWord = vspi.transfer16(wordToSend);
 
	return rcvWord;
}

///////////////////////////////////////////////////////////////////////////////
// void spi::SelectDevice(uint8_t spiDeviceNumber)

void spi::SelectDevice(uint8_t spiDeviceNumber)
{
	uint8_t gpioPinNumber = 0;
	uint8_t bitValue = LOW;
	uint8_t bitNr = 0;

	if (spiDeviceNumber <= SPI_MAX_DEVICENUMBER)
	{
		for (bitNr = 0; bitNr < SPI_N_SELECTBITS; bitNr++)
		{
			gpioPinNumber = SelectPins[bitNr];
			bitValue = LOW;
			if ((spiDeviceNumber & (0x01 << bitNr)) != 0)
			{
				bitValue = HIGH;
			}
			digitalWrite(gpioPinNumber, bitValue);
		}
	}
}

///////////////////////////////////////////////////////////////////////////////
// void spi::DeselectDevice(void)

void spi::DeselectDevice(void)
{
	SelectDevice(SPI_DEVICE_UNUSED);
}
