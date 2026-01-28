#!/usr/bin/env python3
"""
Advanced ESP32 RPC Example - Multi-sensor monitoring

Demonstrates practical use of RPC for sensor monitoring
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import argparse
import logging
from library.rpc_client import RPCClient
from library.config import COMM_USB, RPC_OK, setup_logging, DEBUG_NONE, DEBUG_ERROR, DEBUG_WARNING, DEBUG_INFO, DEBUG_VERBOSE



# Setup logger
logger = logging.getLogger(__name__)


class ESP32Monitor:
    """Monitor ESP32 system and sensors"""
    
    def __init__(self):
        logger.debug("Initializing ESP32Monitor")
        self.client = RPCClient(comm_mode=COMM_USB)
        self.readings = []
    
    def connect(self):
        """Connect to ESP32"""
        logger.info("Connecting to ESP32...")
        success, msg = self.client.connect()
        print(f"Connection: {msg}")
        if success:
            logger.info("Successfully connected")
        else:
            logger.error("Connection failed")
        return success
    
    def disconnect(self):
        """Disconnect from ESP32"""
        logger.info("Disconnecting from ESP32...")
        self.client.disconnect()
        print("Disconnected")
        logger.debug("Disconnected")
    
    def read_sensors(self, iterations=10, interval=1.0):
        """
        Read multiple analog sensors
        
        Args:
            iterations: Number of readings
            interval: Delay between readings in seconds
        """
        logger.info(f"Starting sensor readings: iterations={iterations}, interval={interval}s")
        print(f"\nReading {iterations} sensor samples (interval: {interval}s)")
        print("-" * 60)
        print(f"{'Time(ms)':>10} | {'ADC36':>6} | {'ADC39':>6} | {'Free Mem':>10}")
        print("-" * 60)
        
        for i in range(iterations):
            # Get current time
            result, msg, millis = self.client.getMillis()
            
            # Read analog inputs
            result, msg, adc36 = self.client.analogRead(36)
            result, msg, adc39 = self.client.analogRead(39)
            
            # Get system stats
            result, msg, free_mem = self.client.getFreeMem()
            
            # Store reading
            reading = {
                'time': millis,
                'adc36': adc36,
                'adc39': adc39,
                'free_mem': free_mem
            }
            self.readings.append(reading)
            
            # Print current reading
            print(f"{millis:>10} | {adc36:>6} | {adc39:>6} | {free_mem:>10}")
            
            if i < iterations - 1:
                time.sleep(interval)
        
        print("-" * 60)
    
    def print_statistics(self):
        """Print statistics from readings"""
        if not self.readings:
            print("No readings available")
            return
        
        print("\nSensor Statistics")
        print("-" * 50)
        
        # ADC36 statistics
        adc36_values = [r['adc36'] for r in self.readings if r['adc36'] is not None]
        if adc36_values:
            print(f"ADC36 - Min: {min(adc36_values)}, Max: {max(adc36_values)}, "
                  f"Avg: {sum(adc36_values)/len(adc36_values):.1f}")
        
        # ADC39 statistics
        adc39_values = [r['adc39'] for r in self.readings if r['adc39'] is not None]
        if adc39_values:
            print(f"ADC39 - Min: {min(adc39_values)}, Max: {max(adc39_values)}, "
                  f"Avg: {sum(adc39_values)/len(adc39_values):.1f}")
        
        # Free memory statistics
        mem_values = [r['free_mem'] for r in self.readings if r['free_mem'] is not None]
        if mem_values:
            print(f"Free Memory - Min: {min(mem_values)}, Max: {max(mem_values)}, "
                  f"Avg: {sum(mem_values)/len(mem_values):.0f} bytes")
    
    def test_led_blink(self, pin=2, iterations=3):
        """
        Test LED blink on pin
        
        Args:
            pin: GPIO pin number
            iterations: Number of blinks
        """
        print(f"\nTesting LED blink on pin {pin}")
        print("-" * 50)
        
        # Set pin as output
        result, msg = self.client.pinMode(pin, 1)
        if result != RPC_OK:
            print(f"✗ Failed to set pin mode: {msg}")
            return
        
        for i in range(iterations):
            # LED ON
            result, msg = self.client.digitalWrite(pin, 1)
            print(f"Iteration {i+1}: LED ON ({result}) - {msg}")
            time.sleep(0.5)
            
            # LED OFF
            result, msg = self.client.digitalWrite(pin, 0)
            print(f"Iteration {i+1}: LED OFF ({result}) - {msg}")
            time.sleep(0.5)
        
        print("✓ LED test completed")
    
    def test_pwm_brightness(self, channel=0, pin=32):
        """
        Test PWM brightness control
        
        Args:
            channel: PWM channel
            pin: GPIO pin for PWM output
        """
        print(f"\nTesting PWM brightness control (channel {channel})")
        print("-" * 50)
        
        # Setup PWM
        result, msg = self.client.ledcSetup(channel, 5000, 8)
        if result != RPC_OK:
            print(f"✗ Failed to setup PWM: {msg}")
            return
        
        # Attach GPIO pin to PWM (this would be done in firmware separately)
        # For now, just demonstrate PWM values
        
        duty_values = [0, 85, 170, 255]
        for duty in duty_values:
            result, msg = self.client.ledcWrite(channel, duty)
            brightness_percent = int((duty / 255) * 100)
            print(f"Duty {duty:>3} ({brightness_percent:>3}%) - {msg}")
            time.sleep(0.3)
        
        print("✓ PWM test completed")
    
    def test_pulse_generation(self, channel=0, pin=25):
        """
        Test pulse generation functions
        
        Args:
            channel: Pulse channel (0-3)
            pin: GPIO pin for pulse output
        """
        print(f"\nTesting Pulse Generation (channel {channel}, pin {pin})")
        print("-" * 50)
        
        # Initialize pulse channel
        result, msg = self.client.pulseBegin(channel, pin)
        if result != RPC_OK:
            print(f"✗ Failed to initialize pulse channel: {msg}")
            return
        print(f"✓ Pulse channel {channel} initialized on pin {pin}")
        
        # Single pulse test
        print(f"Generating single 200ms pulse...")
        result, msg = self.client.pulse(channel, 200)
        if result == RPC_OK:
            print(f"✓ Single pulse completed")
        else:
            print(f"✗ Single pulse failed: {msg}")
        
        time.sleep(0.3)
        
        # Single async pulse test
        print(f"Generating async 250ms pulse...")
        result, msg = self.client.pulseAsync(channel, 250)
        if result == RPC_OK:
            print(f"✓ Async pulse started")
            time.sleep(0.1)
            result, msg, pulsing = self.client.isPulsing(channel)
            if result == RPC_OK:
                status = "ACTIVE" if pulsing else "IDLE"
                print(f"  Pulse status: {status}")
        else:
            print(f"✗ Async pulse failed: {msg}")
        
        time.sleep(0.3)
        
        # Multiple pulses (blocking)
        print(f"Generating 5 pulses (100ms on, 100ms off)...")
        result, msg = self.client.generatePulses(channel, 100, 100, 5)
        if result == RPC_OK:
            print(f"✓ Pulse sequence completed")
        else:
            print(f"✗ Pulse sequence failed: {msg}")
        
        time.sleep(0.3)
        
        # Asynchronous pulses
        print(f"Starting async pulse generation (3 pulses, 150ms on, 150ms off)...")
        result, msg = self.client.generatePulsesAsync(channel, 150, 150, 3)
        if result == RPC_OK:
            print(f"✓ Async pulse generation started")
            
            # Check pulse status
            for i in range(5):
                time.sleep(0.2)
                result, msg, pulsing = self.client.isPulsing(channel)
                if result == RPC_OK:
                    status = "ACTIVE" if pulsing else "IDLE"
                    print(f"  Pulse status check {i+1}: {status}")
        else:
            print(f"✗ Async pulse generation failed: {msg}")
        
        print("✓ Pulse test completed")


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='ESP32 RPC Advanced Example - Sensor Monitoring')
    parser.add_argument('-d', '--debug', type=int, choices=[0, 1, 2, 3, 4], default=0,
                        help='Debug level: 0=None, 1=Error, 2=Warning, 3=Info, 4=Verbose (default: 0)')
    parser.add_argument('-l', '--log-file', action='store_true',
                        help='Enable logging to file (rpc_client.log)')
    parser.add_argument('-i', '--iterations', type=int, default=5,
                        help='Number of sensor readings (default: 5)')
    parser.add_argument('--interval', type=float, default=0.5,
                        help='Interval between readings in seconds (default: 0.5)')
    args = parser.parse_args()
    
    # Setup logging based on arguments
    setup_logging(debug_level=args.debug, log_to_file=args.log_file)
    
    logger.info("Starting ESP32 RPC Advanced Example")
    logger.debug(f"Arguments: debug={args.debug}, log_file={args.log_file}, iterations={args.iterations}, interval={args.interval}")
    
    monitor = ESP32Monitor()
    
    # Connect to ESP32
    if not monitor.connect():
        logger.error("Failed to connect to ESP32")
        print("Failed to connect to ESP32")
        return
    
    try:
        # Test LED blink
        monitor.test_led_blink(pin=2, iterations=2)
        
        # Test PWM brightness
        monitor.test_pwm_brightness(channel=0)
        
        # Test pulse generation
        monitor.test_pulse_generation(channel=0, pin=25)
        
        # Read sensors
        monitor.read_sensors(iterations=args.iterations, interval=args.interval)
        
        # Print statistics
        monitor.print_statistics()
        
        logger.info("All tests completed successfully")
        print("\n✓ All tests completed successfully!")
        
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        print("\n\nInterrupted by user")
    except Exception as e:
        logger.exception(f"Error during execution: {e}")
        print(f"\n✗ Error: {e}")
    finally:
        monitor.disconnect()
        logger.info("Advanced example script completed")


if __name__ == "__main__":
    main()
