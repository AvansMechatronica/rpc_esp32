"""
Transport layer for RPC communication (USB or WiFi)
"""

import json
import time
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from .config import CONFIG, RPC_OK, COMM_USB, COMM_WIFI

# Setup logger
logger = logging.getLogger(__name__)

class Transport(ABC):
    """Abstract base class for transport layer"""
    
    @abstractmethod
    def connect(self) -> bool:
        """Connect to device"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from device"""
        pass
    
    @abstractmethod
    def send(self, data: str) -> bool:
        """Send data to device"""
        pass
    
    @abstractmethod
    def recv(self, timeout: float = 2.0) -> Optional[str]:
        """Receive data from device"""
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """Check if connected"""
        pass


class SerialTransport(Transport):
    """USB/Serial transport"""
    
    def __init__(self, port: str = None, baudrate: int = None):
        self.port = port or CONFIG['usb_port']
        self.baudrate = baudrate or CONFIG['usb_baudrate']
        self.serial = None
        self._connected = False
        logger.info(f"SerialTransport initialized: port={self.port}, baudrate={self.baudrate}")
        
    def connect(self) -> bool:
        """Connect to serial port"""
        logger.info(f"Connecting to serial port: {self.port}")
        try:
            import serial
            self.serial = serial.Serial(self.port, self.baudrate, timeout=1)
            #self.serial.setDTR(False)
            #self.serial.setRTS(False)

            # Wait for finishing Reset on ESP32
            time.sleep(5.0)  # Brief wait for port to stabilize
            # Flush input and output buffers to clear any stale data
            self.serial.reset_input_buffer()
            self.serial.reset_output_buffer()
            logger.info("Serial buffers flushed")
            if CONFIG['debug']:
                print("[DEBUG] Serial buffers flushed")
            time.sleep(2)  # Wait for ESP32 to initialize
            self._connected = True
            logger.info(f"Successfully connected to {self.port}")
            if CONFIG['debug']:
                print(f"[DEBUG] Connected to {self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to {self.port}: {e}")
            if CONFIG['debug']:
                print(f"[ERROR] Failed to connect: {e}")
            self._connected = False
            return False
    
    def disconnect(self) -> None:
        """Disconnect from serial port"""
        if self.serial:
            logger.info("Closing serial port connection")
            self.serial.close()
            self._connected = False
            logger.debug("Serial port closed")
            if CONFIG['debug']:
                print("[DEBUG] Disconnected from serial port")
    
    def send(self, data: str) -> bool:
        """Send data via serial"""
        if not self._connected or not self.serial:
            logger.warning("Send attempted while not connected")
            return False
        
        try:
            logger.debug(f"Sending data ({len(data)} bytes): {data[:100]}..." if len(data) > 100 else f"Sending data: {data}")
            self.serial.write((data + '\n').encode())
            if CONFIG['debug']:
                print(f"[DEBUG] Sent: {data}")
            return True
        except Exception as e:
            logger.error(f"Send failed: {e}")
            if CONFIG['debug']:
                print(f"[ERROR] Send failed: {e}")
            return False
    
    def recv(self, timeout: float = 2.0) -> Optional[str]:
        """Receive data via serial"""
        if not self._connected or not self.serial:
            logger.warning("Recv attempted while not connected")
            return None
        
        logger.debug(f"Waiting for response (timeout={timeout}s)...")
        try:
            start_time = time.time()
            while (time.time() - start_time) < timeout:
                if self.serial.in_waiting > 0:
                    response = self.serial.readline().decode().strip()
                    logger.debug(f"Received data ({len(response)} bytes): {response[:100]}..." if len(response) > 100 else f"Received data: {response}")
                    if CONFIG['debug']:
                        print(f"[DEBUG] Received: {response}")
                    return response
                time.sleep(0.01)
            logger.warning(f"Receive timeout after {timeout}s")
            return None
        except Exception as e:
            logger.error(f"Recv failed: {e}")
            if CONFIG['debug']:
                print(f"[ERROR] Recv failed: {e}")
            return None
    
    def is_connected(self) -> bool:
        """Check if serial port is connected"""
        return self._connected and self.serial and self.serial.is_open


class WiFiTransport(Transport):
    """WiFi socket transport"""
    
    def __init__(self, host: str = None, port: int = None):
        self.host = host or CONFIG['wifi_host']
        self.port = port or CONFIG['wifi_port']
        self.socket = None
        self._connected = False
        self._recv_buffer = ""
        logger.info(f"WiFiTransport initialized: host={self.host}, port={self.port}")
        
    def connect(self) -> bool:
        """Connect to WiFi socket"""
        logger.info(f"Connecting to WiFi: {self.host}:{self.port}")
        try:
            import socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(2)
            self.socket.connect((self.host, self.port))
            self._connected = True
            logger.info(f"Successfully connected to {self.host}:{self.port}")
            if CONFIG['debug']:
                print(f"[DEBUG] Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to {self.host}:{self.port}: {e}")
            if CONFIG['debug']:
                print(f"[ERROR] Failed to connect: {e}")
            self._connected = False
            return False
    
    def disconnect(self) -> None:
        """Disconnect from WiFi socket"""
        if self.socket:
            logger.info("Closing WiFi socket connection")
            self.socket.close()
            self._connected = False
            logger.debug("WiFi socket closed")
            if CONFIG['debug']:
                print("[DEBUG] Disconnected from WiFi")
    
    def send(self, data: str) -> bool:
        """Send data via WiFi"""
        if not self._connected or not self.socket:
            logger.warning("Send attempted while not connected")
            return False
        
        try:
            logger.debug(f"Sending data ({len(data)} bytes): {data[:100]}..." if len(data) > 100 else f"Sending data: {data}")
            self.socket.sendall((data + '\n').encode())
            if CONFIG['debug']:
                print(f"[DEBUG] Sent: {data}")
            return True
        except Exception as e:
            logger.error(f"Send failed: {e}")
            if CONFIG['debug']:
                print(f"[ERROR] Send failed: {e}")
            return False
    
    def recv(self, timeout: float = 2.0) -> Optional[str]:
        """Receive data via WiFi"""
        if not self._connected or not self.socket:
            logger.warning("Recv attempted while not connected")
            return None
        
        logger.debug(f"Waiting for response (timeout={timeout}s)...")
        try:
            self.socket.settimeout(timeout)
            end_time = time.time() + timeout
            # Use a small read loop to handle TCP framing (newline terminated)
            while time.time() < end_time:
                # If buffer already has a full line, return it
                if "\n" in self._recv_buffer:
                    line, self._recv_buffer = self._recv_buffer.split("\n", 1)
                    line = line.strip()
                    logger.debug(f"Received data ({len(line)} bytes): {line[:100]}..." if len(line) > 100 else f"Received data: {line}")
                    if CONFIG['debug']:
                        print(f"[DEBUG] Received: {line}")
                    return line if line else None
                try:
                    chunk = self.socket.recv(1024)
                except Exception as e:
                    logger.error(f"Recv failed during read: {e}")
                    if CONFIG['debug']:
                        print(f"[ERROR] Recv failed: {e}")
                    return None
                if not chunk:
                    # No data read; wait briefly
                    time.sleep(0.01)
                    continue
                self._recv_buffer += chunk.decode()
            logger.warning(f"Receive timeout after {timeout}s")
            return None
        except Exception as e:
            logger.error(f"Recv failed: {e}")
            if CONFIG['debug']:
                print(f"[ERROR] Recv failed: {e}")
            return None
    
    def is_connected(self) -> bool:
        """Check if WiFi socket is connected"""
        return self._connected and self.socket is not None


class TransportFactory:
    """Factory for creating transport instances"""
    
    @staticmethod
    def create(comm_mode: int = None, **kwargs) -> Transport:
        """Create transport for the requested mode, allowing overrides (port/host)."""
        mode = comm_mode or CONFIG['comm_mode']
        logger.info(f"Creating transport for mode: {mode} ({'USB' if mode == COMM_USB else 'WiFi' if mode == COMM_WIFI else 'Unknown'}), overrides={kwargs}")
        
        if mode == COMM_USB:
            return SerialTransport(port=kwargs.get('port'), baudrate=kwargs.get('baudrate'))
        elif mode == COMM_WIFI:
            return WiFiTransport(host=kwargs.get('host'), port=kwargs.get('port'))
        else:
            logger.error(f"Unknown communication mode: {mode}")
            raise ValueError(f"Unknown communication mode: {mode}")
