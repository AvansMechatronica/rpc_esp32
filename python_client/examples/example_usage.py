#!/usr/bin/env python3
"""
Example usage of ESP32 RPC Client

This script demonstrates basic usage of the RPC client library
"""

import argparse
import logging
from library.rpc_client import RPCClient
from library.config import COMM_USB, RPC_OK, setup_logging, DEBUG_NONE, DEBUG_ERROR, DEBUG_WARNING, DEBUG_INFO, DEBUG_VERBOSE

# Setup logger
logger = logging.getLogger(__name__)


def print_result(operation, result, message, value=None):
    """Pretty print operation result"""
    status = "✓" if result == RPC_OK else "✗"
    print(f"{status} {operation}: Result code: {result}, Message: {message}", end="")
    if value is not None:
        print(f", Value: {value}", end="")
    print()


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='ESP32 RPC Client Example')
    parser.add_argument('-d', '--debug', type=int, choices=[0, 1, 2, 3, 4], default=0,
                        help='Debug level: 0=None, 1=Error, 2=Warning, 3=Info, 4=Verbose (default: 0)')
    parser.add_argument('-l', '--log-file', action='store_true',
                        help='Enable logging to file (rpc_client.log)')
    parser.add_argument('-p', '--port', default='/dev/ttyUSB0',
                        help='Serial port (default: /dev/ttyUSB0)')
    args = parser.parse_args()
    
    # Setup logging based on arguments
    setup_logging(debug_level=args.debug, log_to_file=args.log_file)
    
    logger.info("Starting ESP32 RPC Client Example")
    logger.debug(f"Arguments: debug={args.debug}, log_file={args.log_file}, port={args.port}")
    
    # Initialize RPC client
    print("Initializing RPC Client...")
    client = RPCClient(comm_mode=COMM_USB)
    
    # Connect to ESP32
    print("Connecting to ESP32...")
    success, message = client.connect()
    
    if not success:
        print(f"✗ Failed to connect: {message}")
        return
    
    print(f"✓ Connected: {message}\n")
    
    try:
        # ===== GPIO Tests =====
        print("=" * 50)
        print("GPIO Operations")
        print("=" * 50)
        
        # Set pin 13 as OUTPUT
        result, msg = client.pinMode(13, 1)
        print_result("pinMode(13, 1)", result, msg)
        
        # Write HIGH to pin 13
        result, msg = client.digitalWrite(13, 1)
        print_result("digitalWrite(13, 1)", result, msg)
        
        # Delay
        result, msg = client.delay(500)
        print_result("delay(500ms)", result, msg)
        
        # Write LOW to pin 13
        result, msg = client.digitalWrite(13, 0)
        print_result("digitalWrite(13, 0)", result, msg)
        
        # Read digital pin
        result, msg, value = client.digitalRead(13)
        print_result("digitalRead(13)", result, msg, value)
        
        print()
        
        # ===== Analog Tests =====
        print("=" * 50)
        print("Analog Operations")
        print("=" * 50)
        
        # Read analog pin (ADC pin on ESP32)
        result, msg, value = client.analogRead(36)
        print_result("analogRead(36)", result, msg, value)
        
        result, msg, value = client.analogRead(39)
        print_result("analogRead(39)", result, msg, value)
        
        print()
        
        # ===== System Information =====
        print("=" * 50)
        print("System Information")
        print("=" * 50)
        
        # Get milliseconds since boot
        result, msg, millis = client.getMillis()
        print_result("getMillis()", result, msg, f"{millis}ms")
        
        # Get free heap memory
        result, msg, free_mem = client.getFreeMem()
        print_result("getFreeMem()", result, msg, f"{free_mem} bytes")
        
        # Get chip ID
        result, msg, chip_id = client.getChipID()
        if chip_id:
            print_result("getChipID()", result, msg, f"0x{chip_id:08X}")
        else:
            print_result("getChipID()", result, msg)
        
        print()
        
        # ===== PWM Tests =====
        print("=" * 50)
        print("PWM Operations")
        print("=" * 50)
        
        # Setup PWM channel 0 at 5kHz with 8-bit resolution
        result, msg = client.ledcSetup(0, 5000, 8)
        print_result("ledcSetup(0, 5000, 8)", result, msg)
        
        # Write PWM values (0-255 for 8-bit)
        for duty in [0, 64, 128, 192, 255]:
            result, msg = client.ledcWrite(0, duty)
            print_result(f"ledcWrite(0, {duty})", result, msg)
        
        print()
        
        # ===== Pulse Library Tests =====
        print("=" * 50)
        print("Pulse Library Operations")
        print("=" * 50)
        
        # Initialize pulse channel 0 on pin 25
        result, msg = client.pulseBegin(0, 25)
        print_result("pulseBegin(0, 25)", result, msg)
        
        # Single pulse test
        result, msg = client.pulse(0, 100)
        print_result("pulse(0, 100ms)", result, msg)
        
        # Single async pulse test
        result, msg = client.pulseAsync(0, 150)
        print_result("pulseAsync(0, 150ms)", result, msg)
        
        # Check if pulsing
        result, msg, pulsing = client.isPulsing(0)
        print_result("isPulsing(0)", result, msg, pulsing)
        
        # Generate multiple pulses (blocking)
        result, msg = client.generatePulses(0, 50, 50, 5)
        print_result("generatePulses(0, 50ms, 50ms, 5 pulses)", result, msg)
        
        # Generate pulses asynchronously (non-blocking)
        result, msg = client.generatePulsesAsync(0, 100, 100, 3)
        print_result("generatePulsesAsync(0, 100ms, 100ms, 3 pulses)", result, msg)
        
        # Query remaining pulses during async run
        result, msg, remaining = client.getRemainingPulses(0)
        print_result("getRemainingPulses(0)", result, msg, remaining)
        
        # Check if still pulsing
        result, msg, pulsing = client.isPulsing(0)
        print_result("isPulsing(0)", result, msg, pulsing)
        
        # Stop pulse
        result, msg = client.stopPulse(0)
        print_result("stopPulse(0)", result, msg)
        
        print()
        
        # ===== Raw Command Test =====
        print("=" * 50)
        print("Raw RPC Command")
        print("=" * 50)
        
        result, msg, data = client.call_raw("millis", {})
        print(f"call_raw('millis', {{}}) -> Result: {result}, Message: {msg}")
        if data:
            print(f"Data: {data}")
        
        print()
        print("=" * 50)
        print("All tests completed!")
        
    except Exception as e:
        logger.exception(f"Error during execution: {e}")
        print(f"✗ Error: {e}")
    
    finally:
        # Always disconnect
        client.disconnect()
        print("\nDisconnected from ESP32")
        logger.info("Example script completed")


if __name__ == "__main__":
    main()
