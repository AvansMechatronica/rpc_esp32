///////////////////////////////////////////////////////////////////////////////
//
// SC18IS606.cpp
//
// copied from https://github.com/maxgerhardt/SC18IS602B-arduino
//
// Original device = SC18IS602, adapted for SC18IS606
//
// Adapted by:	Roel Smeets
// Edit date: 	14-12-2025
//
///////////////////////////////////////////////////////////////////////////////

#ifndef _SC18IS606_H_
#define _SC18IS606_H_

///////////////////////////////////////////////////////////////////////////////
// system #includes

#include <Arduino.h>
#include <Wire.h>

///////////////////////////////////////////////////////////////////////////////
// application #includes

#include <SC18IS606.h>

SC18IS606::SC18IS606(int resetPin, bool a0, bool a1, bool a2)
    : resetPin(resetPin) 
{
    //calculate the module's address here.
    //last 3 bit are the value of the address pin
    address = 0B0101000 | (a2 << 2) | (a1 << 1) | (a0);
}

SC18IS606::~SC18IS606() 
{
}

void SC18IS606::reset()
{
	if (resetPin != -1)
	{
		pinMode(resetPin, OUTPUT);
		// RESET is low active, LOW
		// Generate a high-to-low-to-high transition
		// must be at least 50ns long (t_sa). 1ms is enough.
		digitalWrite(resetPin, HIGH);
		delay(1);
		digitalWrite(resetPin, LOW);
		delay(1);
		digitalWrite(resetPin, HIGH);
	}
}

bool SC18IS606::enableGPIO(int num, bool enable)
{
	// sanity check
	if (num < 0 || num > 2)
	{
		return false;
	}

	// enable this GPIO while leaving the others untouched.
	bitWrite(gpioEnable, num, enable);

	// Send the new enable configuration
	return this->i2c_write(SC18IS606_GPIO_ENABLE_CMD, &gpioEnable, sizeof(gpioEnable));
}

bool SC18IS606::setupGPIO(int num, SC18IS606_GPIOPinMode mode)
{
	// sanity check
	if (num < 0 || num > 2)
		return false;

	// Cast the enum back to the bits
	// mode is a 2-bit wide bitfield
	uint8_t modeAsBitfield = (uint8_t)mode;

	// write 2 the bits into our last config value
	// refer to table 10 in the datasheet
	bitWrite(gpioConfig, 2 * num, modeAsBitfield & 1);
	bitWrite(gpioConfig, 2 * num + 1, modeAsBitfield >> 1);

	return this->i2c_write(SC18IS606_GPIO_CONFIGURATION_CMD, &gpioConfig, sizeof(gpioConfig));
}

bool SC18IS606::writeGPIO(int num, bool val)
{
	if (num < 0 || num > 2)
		return false;
	// Re-write old value
	bitWrite(gpioWrite, num, val);
	return this->i2c_write(SC18IS606_GPIO_WRITE_CMD, &gpioWrite, sizeof(gpioWrite));
}

bool SC18IS606::writeGPIOBank(uint8_t value)
{
	// remember new value
	gpioWrite = value;
	return this->i2c_write(SC18IS606_GPIO_WRITE_CMD, &gpioWrite, sizeof(gpioWrite));
}

bool SC18IS606::writeGPIOBank(bool gpio0, bool gpio1, bool gpio2, bool gpio3)
{
	// Writes all gpio values to the pin
	uint8_t gpioVal = (gpio3 << 3) | (gpio2 << 2) | (gpio1 << 1) | gpio0;
	return writeGPIOBank(gpioVal);
}

bool SC18IS606::readGPIO(int num)
{
	if (num < 0 || num > 2)
		return false;

	// refer chapter 7.1.9
	// issue a read command.
	// this will cause the storage of 1 byte in the data buffer
	if (!this->i2c_write(SC18IS606_GPIO_READ_CMD, nullptr, 0))
		return false;

	// Now try to read the buffer
	uint8_t gpioReadBuf = 0;
	size_t readBytes = this->i2c_read(&gpioReadBuf, sizeof(gpioReadBuf));

	if (readBytes == 0)
	{
		return false;
	}

	// return the bit at the needed position
	return bitRead(gpioReadBuf, num);
}

bool SC18IS606::setLowPowerMode()
{
	return this->i2c_write(SC18IS606_IDLE_CMD, nullptr, 0);
}

bool SC18IS606::clearInterrupt()
{
	return this->i2c_write(SC18IS606_CLEAR_INTERRUPT_CMD, nullptr, 0);
}

bool SC18IS606::i2c_write(uint8_t cmdByte, const uint8_t *data, size_t len)
{
	Wire.beginTransmission(address);
	Wire.write(cmdByte);
	Wire.write(data, len);
	return Wire.endTransmission() == 0;
}

bool SC18IS606::configureSPI(bool lsbFirst, SC18IS606_SPI_Mode spiMode,
							  SC18IS606_SPI_Speed clockSpeed)
{
	// sanity check on parameters
	if (spiMode > SC18IS606_SPIMODE_3)
		return false;
	uint8_t clk = (uint8_t)((uint8_t)(clockSpeed) & 0B11);

	// see chapter 7.1.5
	uint8_t configByte = (lsbFirst << 5) | (spiMode << 2) | clk;
	return this->i2c_write(SC18IS606_CONFIG_SPI_CMD, &configByte, sizeof(configByte));
}

void SC18IS606::begin()
{
	Wire.begin();
}

#ifdef ARDUINO_ARCH_ESP8266
void SC18IS602B::begin(int sda, int scl)
{
	Wire.begin(sda, scl);
}
#endif

uint8_t SC18IS606::spiTransfer(int slaveNum, uint8_t txByte)
{
	uint8_t readBuf = 0;
	this->spiTransfer(slaveNum, &txByte, 1, &readBuf);
	return readBuf;
}

size_t SC18IS606::i2c_read(uint8_t *readBuf, size_t len)
{
	while (Wire.requestFrom(address, len) == 0)
		;
	return Wire.readBytes(readBuf, len);
}

bool SC18IS606::spiTransfer(int slaveNum, const uint8_t *txData, size_t txLen,
							 uint8_t *readBuf)
{
	// sanity check
	if (slaveNum < 0 || slaveNum > 2)
		return false;

	// Overly long data?
	if (txLen > SC18IS606_DATABUFFER_DEPTH)
		return false;

	// the function ID will have the lower 3 bits set to the
	// activated slave selects. We use only 1 at a time here.
	uint8_t functionID = (1 << slaveNum);
	// transmit our TX buffer
	if (!this->i2c_write(functionID, txData, txLen))
		return false;
	// read in the data that came from MISO
	return i2c_read(readBuf, txLen);
}

#endif
