///////////////////////////////////////////////////////////////////////////////
//
// ExtIOLib.h
//
// Authors: 	Roel Smeets
// Edit date: 	13-12-2025
//
///////////////////////////////////////////////////////////////////////////////

#ifndef EXTIOLIB_H
#define EXTIOLIB_H

///////////////////////////////////////////////////////////////////////////////
// system #includes

#include <inttypes.h>
#include <stdbool.h>

///////////////////////////////////////////////////////////////////////////////
// #define's

#define N_EXT_INPUT_BITS	8
#define N_EXT_OUTPUT_BITS	8

///////////////////////////////////////////////////////////////////////////////
// function prototypes

bool extio_Init(void);
bool extio_SetOutput(uint8_t value);
uint8_t extio_GetInput(void);

bool extio_IsBitSet(uint8_t bitNumber);
void extio_SetBit(uint8_t bitNumber, bool bitOn);
bool extio_IsValidBitNumber(uint8_t bitNumber);

bool extio_IsInputConnected(void);
bool extio_IsOutputConnected(void);

#endif	// EXTIOLIB_H
