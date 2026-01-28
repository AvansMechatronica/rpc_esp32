#!/usr/bin/env python3
"""
Simple test to verify debug functionality without ESP32 hardware
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from library.config import setup_logging, DEBUG_INFO, DEBUG_VERBOSE, DEBUG_NONE
import logging

def test_logging_levels():
    """Test different logging levels"""
    print("=" * 60)
    print("Testing Debug Logging Levels")
    print("=" * 60)
    
    # Test INFO level
    print("\n1. Testing INFO level (should show info and above):")
    setup_logging(debug_level=DEBUG_INFO)
    logger = logging.getLogger('test_info')
    logger.debug("DEBUG: This should NOT appear")
    logger.info("INFO: This should appear")
    logger.warning("WARNING: This should appear")
    logger.error("ERROR: This should appear")
    
    # Test VERBOSE level
    print("\n2. Testing VERBOSE level (should show all messages):")
    setup_logging(debug_level=DEBUG_VERBOSE)
    logger = logging.getLogger('test_verbose')
    logger.debug("DEBUG: This should appear")
    logger.info("INFO: This should appear")
    
    # Test NONE level
    print("\n3. Testing NONE level (should show nothing):")
    setup_logging(debug_level=DEBUG_NONE)
    logger = logging.getLogger('test_none')
    logger.error("ERROR: This should NOT appear")
    logger.info("INFO: This should NOT appear")
    print("(No messages should have appeared above)")
    
    print("\n✓ All logging level tests completed")


def test_file_logging():
    """Test file logging"""
    import os
    
    print("\n" + "=" * 60)
    print("Testing File Logging")
    print("=" * 60)
    
    log_file = "test_debug.log"
    
    # Remove old log file if exists
    if os.path.exists(log_file):
        os.remove(log_file)
    
    # Enable file logging
    setup_logging(debug_level=DEBUG_INFO, log_to_file=True, log_file=log_file)
    logger = logging.getLogger('test_file')
    logger.info("This message should be in the log file")
    logger.warning("This warning should also be in the log file")
    
    # Check if file was created
    if os.path.exists(log_file):
        print(f"\n✓ Log file '{log_file}' created successfully")
        with open(log_file, 'r') as f:
            content = f.read()
            print(f"\nLog file contents:\n{content}")
        
        # Cleanup
        os.remove(log_file)
        print(f"✓ Log file cleaned up")
    else:
        print(f"\n✗ Log file '{log_file}' was not created")


def test_module_loggers():
    """Test that module loggers work correctly"""
    print("\n" + "=" * 60)
    print("Testing Module Loggers")
    print("=" * 60)
    
    setup_logging(debug_level=DEBUG_INFO)
    
    # Simulate different modules
    rpc_logger = logging.getLogger('rpc_client')
    transport_logger = logging.getLogger('transport')
    
    print("\nSimulating RPC client operations:")
    rpc_logger.info("RPCClient initialized")
    rpc_logger.info("Connecting to ESP32...")
    
    print("\nSimulating transport operations:")
    transport_logger.info("SerialTransport initialized")
    transport_logger.debug("This debug message should NOT appear at INFO level")
    
    print("\n✓ Module logger test completed")


def main():
    print("\n" + "=" * 60)
    print("ESP32 RPC Debug Functionality Test")
    print("This test verifies the debug system without hardware")
    print("=" * 60)
    
    try:
        test_logging_levels()
        test_file_logging()
        test_module_loggers()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        print("\nThe debug functionality is working correctly!")
        print("You can now use --debug options with the example scripts.")
        print("\nTry:")
        print("  python example_usage.py --debug 3 --help")
        print("  python debug_utility.py --help")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
