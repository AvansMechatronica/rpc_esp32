#!/usr/bin/env python3
"""
ESP32 RPC Debug Utility

Interactive debugging tool for ESP32 RPC communication
Provides detailed logging and connection diagnostics
"""

import argparse
import logging
import json
import time
from rpc_client import RPCClient
from config import (
    COMM_USB, COMM_WIFI, RPC_OK, 
    setup_logging, DEBUG_NONE, DEBUG_ERROR, DEBUG_WARNING, DEBUG_INFO, DEBUG_VERBOSE
)

# Setup logger
logger = logging.getLogger(__name__)


def test_connection(client):
    """Test basic connection to ESP32"""
    print("\n" + "=" * 60)
    print("CONNECTION TEST")
    print("=" * 60)
    
    logger.info("Testing connection to ESP32...")
    success, msg = client.connect()
    
    if success:
        print(f"✓ Connection successful: {msg}")
        logger.info("Connection test passed")
        return True
    else:
        print(f"✗ Connection failed: {msg}")
        logger.error("Connection test failed")
        return False


def test_system_info(client):
    """Test system information retrieval"""
    print("\n" + "=" * 60)
    print("SYSTEM INFORMATION TEST")
    print("=" * 60)
    
    logger.info("Retrieving system information...")
    
    # Get chip ID
    result, msg, chip_id = client.getChipID()
    if result == RPC_OK:
        print(f"✓ Chip ID: 0x{chip_id:08X}")
        logger.info(f"Chip ID retrieved: 0x{chip_id:08X}")
    else:
        print(f"✗ Failed to get chip ID: {msg}")
        logger.error(f"Failed to get chip ID: {msg}")
    
    # Get free memory
    result, msg, free_mem = client.getFreeMem()
    if result == RPC_OK:
        print(f"✓ Free Memory: {free_mem} bytes ({free_mem/1024:.2f} KB)")
        logger.info(f"Free memory: {free_mem} bytes")
    else:
        print(f"✗ Failed to get free memory: {msg}")
        logger.error(f"Failed to get free memory: {msg}")
    
    # Get uptime
    result, msg, millis = client.getMillis()
    if result == RPC_OK:
        uptime_sec = millis / 1000
        print(f"✓ Uptime: {millis} ms ({uptime_sec:.2f} seconds)")
        logger.info(f"Uptime: {millis} ms")
    else:
        print(f"✗ Failed to get uptime: {msg}")
        logger.error(f"Failed to get uptime: {msg}")


def test_gpio_operations(client, pin=13):
    """Test GPIO read/write operations"""
    print("\n" + "=" * 60)
    print(f"GPIO OPERATIONS TEST (Pin {pin})")
    print("=" * 60)
    
    logger.info(f"Testing GPIO operations on pin {pin}...")
    
    # Set as output
    result, msg = client.pinMode(pin, 1)
    if result == RPC_OK:
        print(f"✓ Set pin {pin} as OUTPUT")
        logger.debug(f"Pin {pin} set as OUTPUT")
    else:
        print(f"✗ Failed to set pinMode: {msg}")
        logger.error(f"Failed to set pinMode: {msg}")
        return
    
    # Write HIGH
    result, msg = client.digitalWrite(pin, 1)
    if result == RPC_OK:
        print(f"✓ Write HIGH to pin {pin}")
        logger.debug(f"Written HIGH to pin {pin}")
    else:
        print(f"✗ Failed to write HIGH: {msg}")
        logger.error(f"Failed to write HIGH: {msg}")
    
    time.sleep(0.5)
    
    # Write LOW
    result, msg = client.digitalWrite(pin, 0)
    if result == RPC_OK:
        print(f"✓ Write LOW to pin {pin}")
        logger.debug(f"Written LOW to pin {pin}")
    else:
        print(f"✗ Failed to write LOW: {msg}")
        logger.error(f"Failed to write LOW: {msg}")


def test_analog_operations(client, pin=36):
    """Test analog read operations"""
    print("\n" + "=" * 60)
    print(f"ANALOG OPERATIONS TEST (Pin {pin})")
    print("=" * 60)
    
    logger.info(f"Testing analog read on pin {pin}...")
    
    # Read analog value multiple times
    readings = []
    for i in range(5):
        result, msg, value = client.analogRead(pin)
        if result == RPC_OK:
            readings.append(value)
            voltage = (value / 4095.0) * 3.3
            print(f"  Reading {i+1}: {value} (≈{voltage:.2f}V)")
            logger.debug(f"Analog reading {i+1}: {value}")
        else:
            print(f"✗ Failed to read analog: {msg}")
            logger.error(f"Failed to read analog: {msg}")
        time.sleep(0.1)
    
    if readings:
        avg = sum(readings) / len(readings)
        print(f"\n✓ Average reading: {avg:.1f}")
        logger.info(f"Average analog reading: {avg:.1f}")


def test_communication_speed(client, iterations=10):
    """Test RPC communication speed"""
    print("\n" + "=" * 60)
    print(f"COMMUNICATION SPEED TEST ({iterations} iterations)")
    print("=" * 60)
    
    logger.info(f"Testing communication speed with {iterations} iterations...")
    
    times = []
    for i in range(iterations):
        start_time = time.time()
        result, msg, millis = client.getMillis()
        elapsed = (time.time() - start_time) * 1000  # Convert to ms
        
        if result == RPC_OK:
            times.append(elapsed)
            logger.debug(f"Iteration {i+1}: {elapsed:.2f}ms")
        else:
            print(f"✗ Request {i+1} failed: {msg}")
            logger.error(f"Request {i+1} failed: {msg}")
    
    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"✓ Response times:")
        print(f"  Average: {avg_time:.2f}ms")
        print(f"  Min: {min_time:.2f}ms")
        print(f"  Max: {max_time:.2f}ms")
        logger.info(f"Communication speed - Avg: {avg_time:.2f}ms, Min: {min_time:.2f}ms, Max: {max_time:.2f}ms")


def interactive_mode(client):
    """Interactive command mode"""
    print("\n" + "=" * 60)
    print("INTERACTIVE MODE")
    print("=" * 60)
    print("Enter RPC commands in JSON format or 'quit' to exit")
    print("Example: {\"method\": \"millis\", \"params\": {}}")
    print("=" * 60)
    
    logger.info("Entering interactive mode...")
    
    while True:
        try:
            cmd = input("\nRPC> ").strip()
            
            if cmd.lower() in ['quit', 'exit', 'q']:
                logger.info("Exiting interactive mode")
                break
            
            if not cmd:
                continue
            
            try:
                request = json.loads(cmd)
                method = request.get('method')
                params = request.get('params', {})
                
                logger.debug(f"Interactive command: method={method}, params={params}")
                
                result, msg, data = client._send_command(method, params)
                
                print(f"\nResult: {result}")
                print(f"Message: {msg}")
                if data:
                    print(f"Data: {json.dumps(data, indent=2)}")
                
                logger.info(f"Interactive command result: {result}, {msg}")
                
            except json.JSONDecodeError as e:
                print(f"✗ Invalid JSON: {e}")
                logger.warning(f"Invalid JSON in interactive mode: {e}")
                
        except KeyboardInterrupt:
            logger.info("Interactive mode interrupted")
            print("\n")
            break


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='ESP32 RPC Debug Utility')
    parser.add_argument('-d', '--debug', type=int, choices=[0, 1, 2, 3, 4], default=3,
                        help='Debug level: 0=None, 1=Error, 2=Warning, 3=Info, 4=Verbose (default: 3)')
    parser.add_argument('-l', '--log-file', action='store_true',
                        help='Enable logging to file (rpc_client.log)')
    parser.add_argument('-m', '--mode', choices=['usb', 'wifi'], default='usb',
                        help='Communication mode (default: usb)')
    parser.add_argument('-p', '--port', default='/dev/ttyUSB0',
                        help='Serial port for USB mode (default: /dev/ttyUSB0)')
    parser.add_argument('--host', default='192.168.1.100',
                        help='WiFi host address (default: 192.168.1.100)')
    parser.add_argument('--wifi-port', type=int, default=5000,
                        help='WiFi port (default: 5000)')
    parser.add_argument('-t', '--test', choices=['all', 'connection', 'system', 'gpio', 'analog', 'speed', 'interactive'],
                        default='all', help='Test to run (default: all)')
    parser.add_argument('--gpio-pin', type=int, default=13,
                        help='GPIO pin for testing (default: 13)')
    parser.add_argument('--adc-pin', type=int, default=36,
                        help='ADC pin for testing (default: 36)')
    
    args = parser.parse_args()
    
    # Setup logging based on arguments
    setup_logging(debug_level=args.debug, log_to_file=args.log_file)
    
    logger.info("Starting ESP32 RPC Debug Utility")
    logger.debug(f"Arguments: {vars(args)}")
    
    # Initialize RPC client
    comm_mode = COMM_USB if args.mode == 'usb' else COMM_WIFI
    print(f"\nInitializing RPC Client in {'USB' if comm_mode == COMM_USB else 'WiFi'} mode...")
    client = RPCClient(comm_mode=comm_mode)
    
    # Update configuration if needed
    if args.mode == 'usb':
        from config import CONFIG
        CONFIG['usb_port'] = args.port
        logger.info(f"USB port set to: {args.port}")
    else:
        from config import CONFIG
        CONFIG['wifi_host'] = args.host
        CONFIG['wifi_port'] = args.wifi_port
        logger.info(f"WiFi configured: {args.host}:{args.wifi_port}")
    
    try:
        # Test connection
        if not test_connection(client):
            logger.error("Connection test failed, exiting")
            return
        
        # Run selected tests
        if args.test in ['all', 'system']:
            test_system_info(client)
        
        if args.test in ['all', 'gpio']:
            test_gpio_operations(client, args.gpio_pin)
        
        if args.test in ['all', 'analog']:
            test_analog_operations(client, args.adc_pin)
        
        if args.test in ['all', 'speed']:
            test_communication_speed(client)
        
        if args.test == 'interactive':
            interactive_mode(client)
        
        print("\n" + "=" * 60)
        print("DEBUG UTILITY COMPLETED")
        print("=" * 60)
        logger.info("Debug utility completed successfully")
        
    except KeyboardInterrupt:
        logger.warning("Debug utility interrupted by user")
        print("\n\nInterrupted by user")
    except Exception as e:
        logger.exception(f"Error during debug utility execution: {e}")
        print(f"\n✗ Error: {e}")
    finally:
        client.disconnect()
        print("\nDisconnected from ESP32")
        logger.info("Debug utility finished")


if __name__ == "__main__":
    main()
