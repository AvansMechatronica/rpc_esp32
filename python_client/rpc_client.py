"""
ESP32 RPC Client Library

Provides easy-to-use interface for calling RPC functions on ESP32
"""

import json
import logging
from typing import Optional, Dict, Any, Tuple
from transport import Transport, TransportFactory
from config import CONFIG, RPC_OK, COMM_USB, RPC_ERROR_TIMEOUT, get_result_message

# Setup logger
logger = logging.getLogger(__name__)


class RPCClient:
    """RPC Client for communicating with ESP32"""
    
    def __init__(self, comm_mode: int = None, **kwargs):
        """
        Initialize RPC Client
        
        Args:
            comm_mode: COMM_USB (0) or COMM_WIFI (1)
            **kwargs: Additional arguments for transport (e.g., port, host)
        """
        logger.info(f"Initializing RPCClient with comm_mode={comm_mode}, kwargs={kwargs}")
        self.transport = TransportFactory.create(comm_mode, **kwargs)
        self._connected = False
        self._request_id = 0
        logger.debug(f"RPCClient initialized with transport: {type(self.transport).__name__}")
        
    def connect(self) -> Tuple[bool, str]:
        """
        Connect to ESP32
        
        Returns:
            (success, message) tuple
        """
        logger.info("Attempting to connect to ESP32...")
        if self.transport.connect():
            self._connected = True
            logger.info("Successfully connected to ESP32")
            return True, "Connected successfully"
        else:
            logger.error("Failed to connect to ESP32")
            return False, "Failed to connect"
    
    def disconnect(self) -> None:
        """Disconnect from ESP32"""
        logger.info("Disconnecting from ESP32...")
        self.transport.disconnect()
        self._connected = False
        logger.debug("Disconnected from ESP32")
    
    def is_connected(self) -> bool:
        """Check if connected"""
        return self._connected and self.transport.is_connected()
    
    def _send_command(self, method: str, params: Dict[str, Any] = None) -> Tuple[int, str, Dict[str, Any]]:
        """
        Send RPC command to ESP32
        
        Returns:
            (result_code, message, data) tuple
        """
        logger.debug(f"_send_command called: method={method}, params={params}")
        
        if not self.is_connected():
            logger.warning("Command attempted while not connected")
            return RPC_ERROR_TIMEOUT, "Not connected to device", {}
        
        # Build request
        request = {
            "method": method,
            "params": params or {}
        }
        
        request_str = json.dumps(request)
        logger.debug(f"Request JSON: {request_str}")
        
        # Send request
        if not self.transport.send(request_str):
            logger.error(f"Failed to send command: {method}")
            return RPC_ERROR_TIMEOUT, "Failed to send command", {}
        
        logger.debug(f"Command sent successfully: {method}")
        
        # Receive response
        response_str = self.transport.recv(CONFIG['timeout'])
        if response_str is None:
            logger.error(f"No response received for command: {method}")
            return RPC_ERROR_TIMEOUT, "No response from device", {}
        
        logger.debug(f"Response received: {response_str}")
        
        try:
            response = json.loads(response_str)
            result_code = response.get('result', RPC_ERROR_TIMEOUT)
            message = response.get('message', get_result_message(result_code))
            data = response.get('data', {})
            
            if result_code == RPC_OK:
                logger.debug(f"Command successful: {method}, data={data}")
            else:
                logger.warning(f"Command failed: {method}, code={result_code}, msg={message}")
            
            return result_code, message, data
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response: {response_str}, error: {e}")
            return RPC_ERROR_TIMEOUT, "Invalid response format", {}
    
    # GPIO Functions
    def pinMode(self, pin: int, mode: int) -> Tuple[int, str]:
        """
        Set pin mode (INPUT=0, OUTPUT=1, INPUT_PULLUP=2)
        
        Returns:
            (result_code, message) tuple
        """
        result, msg, _ = self._send_command("pinMode", {"pin": pin, "mode": mode})
        return result, msg
    
    def digitalWrite(self, pin: int, value: int) -> Tuple[int, str]:
        """
        Write digital value to pin (0 or 1)
        
        Returns:
            (result_code, message) tuple
        """
        result, msg, _ = self._send_command("digitalWrite", {"pin": pin, "value": value})
        return result, msg
    
    def digitalRead(self, pin: int) -> Tuple[int, str, Optional[int]]:
        """
        Read digital value from pin
        
        Returns:
            (result_code, message, value) tuple
        """
        result, msg, data = self._send_command("digitalRead", {"pin": pin})
        value = data.get('value') if (result == RPC_OK and data) else None
        return result, msg, value
    
    def analogWrite(self, pin: int, value: int) -> Tuple[int, str]:
        """
        Write PWM value to pin (0-255)
        
        Returns:
            (result_code, message) tuple
        """
        result, msg, _ = self._send_command("analogWrite", {"pin": pin, "value": value})
        return result, msg
    
    def analogRead(self, pin: int) -> Tuple[int, str, Optional[int]]:
        """
        Read analog value from pin (0-4095 on ESP32)
        
        Returns:
            (result_code, message, value) tuple
        """
        result, msg, data = self._send_command("analogRead", {"pin": pin})
        value = data.get('value') if (result == RPC_OK and data) else None
        return result, msg, value
    
    # System Functions
    def delay(self, ms: int) -> Tuple[int, str]:
        """
        Delay for specified milliseconds
        
        Returns:
            (result_code, message) tuple
        """
        result, msg, _ = self._send_command("delay", {"ms": ms})
        return result, msg
    
    def getMillis(self) -> Tuple[int, str, Optional[int]]:
        """
        Get milliseconds since boot
        
        Returns:
            (result_code, message, millis) tuple
        """
        result, msg, data = self._send_command("millis", {})
        value = data.get('millis') if (result == RPC_OK and data) else None
        return result, msg, value
    
    def getFreeMem(self) -> Tuple[int, str, Optional[int]]:
        """
        Get free heap memory
        
        Returns:
            (result_code, message, free_mem) tuple
        """
        result, msg, data = self._send_command("freeMem", {})
        value = data.get('free_heap') if (result == RPC_OK and data) else None
        return result, msg, value
    
    def getChipID(self) -> Tuple[int, str, Optional[int]]:
        """
        Get ESP32 chip ID
        
        Returns:
            (result_code, message, chip_id) tuple
        """
        result, msg, data = self._send_command("chipID", {})
        value = data.get('chip_id') if (result == RPC_OK and data) else None
        return result, msg, value
    
    # PWM Functions
    def ledcSetup(self, channel: int, freq: int, bits: int) -> Tuple[int, str]:
        """
        Setup PWM channel
        
        Args:
            channel: PWM channel (0-15)
            freq: Frequency in Hz
            bits: Resolution in bits (1-16)
        
        Returns:
            (result_code, message) tuple
        """
        result, msg, _ = self._send_command("ledcSetup", {
            "channel": channel,
            "freq": freq,
            "bits": bits
        })
        return result, msg
    
    def ledcWrite(self, channel: int, duty: int) -> Tuple[int, str]:
        """
        Write PWM duty cycle
        
        Args:
            channel: PWM channel (0-15)
            duty: Duty cycle (0 - 2^bits - 1)
        
        Returns:
            (result_code, message) tuple
        """
        result, msg, _ = self._send_command("ledcWrite", {
            "channel": channel,
            "duty": duty
        })
        return result, msg
    
    # Pulse Library Functions
    def pulseBegin(self, channel: int, pin: int) -> Tuple[int, str]:
        """
        Initialize pulse channel with pin
        
        Args:
            channel: Pulse channel (0-3)
            pin: GPIO pin number
        
        Returns:
            (result_code, message) tuple
        """
        result, msg, _ = self._send_command("pulseBegin", {
            "channel": channel,
            "pin": pin
        })
        return result, msg
    
    def pulse(self, channel: int, duration_ms: int) -> Tuple[int, str]:
        """
        Generate a single pulse (blocking)
        
        Args:
            channel: Pulse channel (0-3)
            duration_ms: Duration of pulse in milliseconds
        
        Returns:
            (result_code, message) tuple
        """
        result, msg, _ = self._send_command("pulse", {
            "channel": channel,
            "duration_ms": duration_ms
        })
        return result, msg
    
    def pulseAsync(self, channel: int, duration_ms: int) -> Tuple[int, str]:
        """
        Generate a single pulse asynchronously (non-blocking)
        Returns immediately, pulse executes in background
        
        Args:
            channel: Pulse channel (0-3)
            duration_ms: Duration of pulse in milliseconds
        
        Returns:
            (result_code, message) tuple
        """
        result, msg, _ = self._send_command("pulseAsync", {
            "channel": channel,
            "duration_ms": duration_ms
        })
        return result, msg
    
    def isPulsing(self, channel: int) -> Tuple[int, str, Optional[bool]]:
        """
        Check if channel is currently pulsing
        
        Args:
            channel: Pulse channel (0-3)
        
        Returns:
            (result_code, message, pulsing) tuple
        """
        result, msg, data = self._send_command("isPulsing", {"channel": channel})
        pulsing = data.get('pulsing') if (result == RPC_OK and data) else None
        return result, msg, pulsing
    
    def stopPulse(self, channel: int) -> Tuple[int, str]:
        """
        Stop pulsing on channel
        
        Args:
            channel: Pulse channel (0-3)
        
        Returns:
            (result_code, message) tuple
        """
        result, msg, _ = self._send_command("stopPulse", {"channel": channel})
        return result, msg
    
    def generatePulses(self, channel: int, pulse_width_ms: int, pause_width_ms: int, pulse_count: int) -> Tuple[int, str]:
        """
        Generate multiple pulses (blocking)
        
        Args:
            channel: Pulse channel (0-3)
            pulse_width_ms: Width of each pulse in milliseconds
            pause_width_ms: Pause between pulses in milliseconds
            pulse_count: Number of pulses to generate
        
        Returns:
            (result_code, message) tuple
        """
        result, msg, _ = self._send_command("generatePulses", {
            "channel": channel,
            "pulse_width_ms": pulse_width_ms,
            "pause_width_ms": pause_width_ms,
            "pulse_count": pulse_count
        })
        return result, msg
    
    def generatePulsesAsync(self, channel: int, pulse_width_ms: int, pause_width_ms: int, pulse_count: int) -> Tuple[int, str]:
        """
        Generate multiple pulses asynchronously (non-blocking)
        Must call pulseTick() periodically to update pulse state
        
        Args:
            channel: Pulse channel (0-3)
            pulse_width_ms: Width of each pulse in milliseconds
            pause_width_ms: Pause between pulses in milliseconds
            pulse_count: Number of pulses to generate
        
        Returns:
            (result_code, message) tuple
        """
        result, msg, _ = self._send_command("generatePulsesAsync", {
            "channel": channel,
            "pulse_width_ms": pulse_width_ms,
            "pause_width_ms": pause_width_ms,
            "pulse_count": pulse_count
        })
        return result, msg
    
    def pulseTick(self, channel: int) -> Tuple[int, str]:
        """
        Update pulse state for async pulse generation
        Must be called periodically when using generatePulsesAsync
        
        Args:
            channel: Pulse channel (0-3)
        
        Returns:
            (result_code, message) tuple
        """
        result, msg, _ = self._send_command("pulseTick", {"channel": channel})
        return result, msg
    
    # Utility
    def call_raw(self, method: str, params: Dict[str, Any] = None) -> Tuple[int, str, Dict[str, Any]]:
        """
        Call raw RPC method
        
        Returns:
            (result_code, message, data) tuple
        """
        return self._send_command(method, params or {})
