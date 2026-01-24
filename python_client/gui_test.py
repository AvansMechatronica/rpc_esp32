"""
ESP32 RPC GUI Test Application
Provides interactive GUI for testing RPC functions
"""

import sys
import json
from tkinter import *
from tkinter import ttk, messagebox, scrolledtext
from rpc_client import RPCClient
from config import COMM_USB, COMM_WIFI, RPC_OK, CONFIG


class RPCTestGUI:
    """GUI for testing ESP32 RPC functions"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("ESP32 RPC Test Client")
        self.root.geometry("1000x700")
        
        self.client = None
        self.comm_mode = COMM_USB
        
        self.setup_ui()
        self.update_connection_status()
    
    def setup_ui(self):
        """Setup UI elements"""
        
        # Connection Frame
        conn_frame = ttk.LabelFrame(self.root, text="Connection Settings", padding=10)
        conn_frame.pack(fill=X, padx=10, pady=5)
        
        # Communication Mode
        ttk.Label(conn_frame, text="Mode:").grid(row=0, column=0, sticky=W)
        self.mode_var = StringVar(value="USB")
        mode_combo = ttk.Combobox(conn_frame, textvariable=self.mode_var, 
                                  values=["USB", "WiFi"], state="readonly", width=15)
        mode_combo.grid(row=0, column=1, padx=5)
        mode_combo.bind("<<ComboboxSelected>>", self.on_mode_changed)
        
        # USB Port
        ttk.Label(conn_frame, text="USB Port:").grid(row=0, column=2, sticky=W)
        self.usb_port_var = StringVar(value="/dev/ttyUSB0")
        ttk.Entry(conn_frame, textvariable=self.usb_port_var, width=15).grid(row=0, column=3, padx=5)
        
        # WiFi Host
        ttk.Label(conn_frame, text="WiFi Host:").grid(row=1, column=0, sticky=W)
        self.wifi_host_var = StringVar(value="192.168.1.100")
        ttk.Entry(conn_frame, textvariable=self.wifi_host_var, width=15).grid(row=1, column=1, padx=5)
        
        # WiFi Port
        ttk.Label(conn_frame, text="WiFi Port:").grid(row=1, column=2, sticky=W)
        self.wifi_port_var = StringVar(value="5000")
        ttk.Entry(conn_frame, textvariable=self.wifi_port_var, width=15).grid(row=1, column=3, padx=5)
        
        # Connect Button
        self.connect_btn = ttk.Button(conn_frame, text="Connect", command=self.connect)
        self.connect_btn.grid(row=2, column=0, pady=10, sticky=EW)
        
        self.disconnect_btn = ttk.Button(conn_frame, text="Disconnect", command=self.disconnect, state=DISABLED)
        self.disconnect_btn.grid(row=2, column=1, padx=5, sticky=EW)
        
        # Connection Status
        self.status_label = ttk.Label(conn_frame, text="Disconnected", foreground="red")
        self.status_label.grid(row=2, column=2, columnspan=2, sticky=W, padx=5)
        
        # Notebook for different function categories
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        # GPIO Tab
        self.setup_gpio_tab(notebook)
        
        # System Tab
        self.setup_system_tab(notebook)
        
        # PWM Tab
        self.setup_pwm_tab(notebook)
        
        # Pulse Library Tab
        self.setup_pulse_tab(notebook)
        
        # Raw Command Tab
        self.setup_raw_tab(notebook)
        
        # Output Frame
        output_frame = ttk.LabelFrame(self.root, text="Output", padding=5)
        output_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        self.output = scrolledtext.ScrolledText(output_frame, height=8, state=DISABLED)
        self.output.pack(fill=BOTH, expand=True)
        
        # Clear Output Button
        ttk.Button(output_frame, text="Clear Output", command=self.clear_output).pack(pady=5)
    
    def setup_gpio_tab(self, notebook):
        """Setup GPIO functions tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="GPIO")
        
        # pinMode
        ttk.Label(frame, text="pinMode").pack(anchor=W, padx=10, pady=5)
        gpio_frame = ttk.Frame(frame)
        gpio_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Label(gpio_frame, text="Pin:").pack(side=LEFT, padx=5)
        self.pin_var = StringVar(value="13")
        ttk.Entry(gpio_frame, textvariable=self.pin_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Label(gpio_frame, text="Mode (0=IN, 1=OUT, 2=PULLUP):").pack(side=LEFT, padx=5)
        self.mode_pin_var = StringVar(value="1")
        ttk.Entry(gpio_frame, textvariable=self.mode_pin_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Button(gpio_frame, text="pinMode", 
                   command=lambda: self.execute_gpio_pinmode()).pack(side=LEFT, padx=5)
        
        # digitalWrite
        ttk.Label(frame, text="digitalWrite").pack(anchor=W, padx=10, pady=5)
        dig_frame = ttk.Frame(frame)
        dig_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Label(dig_frame, text="Pin:").pack(side=LEFT, padx=5)
        self.dpin_var = StringVar(value="13")
        ttk.Entry(dig_frame, textvariable=self.dpin_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Label(dig_frame, text="Value (0 or 1):").pack(side=LEFT, padx=5)
        self.dvalue_var = StringVar(value="1")
        ttk.Entry(dig_frame, textvariable=self.dvalue_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Button(dig_frame, text="digitalWrite", 
                   command=lambda: self.execute_digitalWrite()).pack(side=LEFT, padx=5)
        
        # digitalRead
        ttk.Label(frame, text="digitalRead").pack(anchor=W, padx=10, pady=5)
        read_frame = ttk.Frame(frame)
        read_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Label(read_frame, text="Pin:").pack(side=LEFT, padx=5)
        self.read_pin_var = StringVar(value="13")
        ttk.Entry(read_frame, textvariable=self.read_pin_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Button(read_frame, text="digitalRead", 
                   command=lambda: self.execute_digitalRead()).pack(side=LEFT, padx=5)
        
        # analogRead
        ttk.Label(frame, text="analogRead").pack(anchor=W, padx=10, pady=5)
        aread_frame = ttk.Frame(frame)
        aread_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Label(aread_frame, text="Pin:").pack(side=LEFT, padx=5)
        self.aread_pin_var = StringVar(value="36")
        ttk.Entry(aread_frame, textvariable=self.aread_pin_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Button(aread_frame, text="analogRead", 
                   command=lambda: self.execute_analogRead()).pack(side=LEFT, padx=5)
    
    def setup_system_tab(self, notebook):
        """Setup System functions tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="System")
        
        # delay
        ttk.Label(frame, text="delay (ms)").pack(anchor=W, padx=10, pady=5)
        delay_frame = ttk.Frame(frame)
        delay_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Label(delay_frame, text="Milliseconds:").pack(side=LEFT, padx=5)
        self.delay_var = StringVar(value="1000")
        ttk.Entry(delay_frame, textvariable=self.delay_var, width=10).pack(side=LEFT, padx=5)
        
        ttk.Button(delay_frame, text="delay", 
                   command=lambda: self.execute_delay()).pack(side=LEFT, padx=5)
        
        # getMillis
        ttk.Label(frame, text="System Information").pack(anchor=W, padx=10, pady=5)
        info_frame = ttk.Frame(frame)
        info_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Button(info_frame, text="Get Millis", 
                   command=lambda: self.execute_getMillis()).pack(side=LEFT, padx=5)
        
        ttk.Button(info_frame, text="Get Free Memory", 
                   command=lambda: self.execute_getFreeMem()).pack(side=LEFT, padx=5)
        
        ttk.Button(info_frame, text="Get Chip ID", 
                   command=lambda: self.execute_getChipID()).pack(side=LEFT, padx=5)
    
    def setup_pwm_tab(self, notebook):
        """Setup PWM functions tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="PWM")
        
        # ledcSetup
        ttk.Label(frame, text="ledcSetup").pack(anchor=W, padx=10, pady=5)
        setup_frame = ttk.Frame(frame)
        setup_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Label(setup_frame, text="Channel:").pack(side=LEFT, padx=5)
        self.pwm_channel_var = StringVar(value="0")
        ttk.Entry(setup_frame, textvariable=self.pwm_channel_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Label(setup_frame, text="Freq (Hz):").pack(side=LEFT, padx=5)
        self.pwm_freq_var = StringVar(value="5000")
        ttk.Entry(setup_frame, textvariable=self.pwm_freq_var, width=10).pack(side=LEFT, padx=5)
        
        ttk.Label(setup_frame, text="Bits:").pack(side=LEFT, padx=5)
        self.pwm_bits_var = StringVar(value="8")
        ttk.Entry(setup_frame, textvariable=self.pwm_bits_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Button(setup_frame, text="Setup", 
                   command=lambda: self.execute_ledcSetup()).pack(side=LEFT, padx=5)
        
        # ledcWrite
        ttk.Label(frame, text="ledcWrite").pack(anchor=W, padx=10, pady=5)
        write_frame = ttk.Frame(frame)
        write_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Label(write_frame, text="Channel:").pack(side=LEFT, padx=5)
        self.pwm_write_channel_var = StringVar(value="0")
        ttk.Entry(write_frame, textvariable=self.pwm_write_channel_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Label(write_frame, text="Duty:").pack(side=LEFT, padx=5)
        self.pwm_duty_var = StringVar(value="128")
        ttk.Entry(write_frame, textvariable=self.pwm_duty_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Button(write_frame, text="Write", 
                   command=lambda: self.execute_ledcWrite()).pack(side=LEFT, padx=5)
    
    def setup_pulse_tab(self, notebook):
        """Setup Pulse Library functions tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Pulse Library")
        
        # pulseBegin
        ttk.Label(frame, text="Initialize Pulse Channel").pack(anchor=W, padx=10, pady=5)
        begin_frame = ttk.Frame(frame)
        begin_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Label(begin_frame, text="Channel (0-3):").pack(side=LEFT, padx=5)
        self.pulse_channel_var = StringVar(value="0")
        ttk.Entry(begin_frame, textvariable=self.pulse_channel_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Label(begin_frame, text="Pin:").pack(side=LEFT, padx=5)
        self.pulse_pin_var = StringVar(value="25")
        ttk.Entry(begin_frame, textvariable=self.pulse_pin_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Button(begin_frame, text="Begin", 
                   command=lambda: self.execute_pulseBegin()).pack(side=LEFT, padx=5)
        
        # Single pulse
        ttk.Label(frame, text="Single Pulse (blocking)").pack(anchor=W, padx=10, pady=5)
        pulse_frame = ttk.Frame(frame)
        pulse_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Label(pulse_frame, text="Channel:").pack(side=LEFT, padx=5)
        self.pulse_single_channel_var = StringVar(value="0")
        ttk.Entry(pulse_frame, textvariable=self.pulse_single_channel_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Label(pulse_frame, text="Duration (ms):").pack(side=LEFT, padx=5)
        self.pulse_duration_var = StringVar(value="100")
        ttk.Entry(pulse_frame, textvariable=self.pulse_duration_var, width=10).pack(side=LEFT, padx=5)
        
        ttk.Button(pulse_frame, text="Pulse", 
                   command=lambda: self.execute_pulse()).pack(side=LEFT, padx=5)
        
        # Single async pulse
        ttk.Label(frame, text="Single Async Pulse (non-blocking)").pack(anchor=W, padx=10, pady=5)
        async_pulse_frame = ttk.Frame(frame)
        async_pulse_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Label(async_pulse_frame, text="Channel:").pack(side=LEFT, padx=5)
        self.pulse_async_single_channel_var = StringVar(value="0")
        ttk.Entry(async_pulse_frame, textvariable=self.pulse_async_single_channel_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Label(async_pulse_frame, text="Duration (ms):").pack(side=LEFT, padx=5)
        self.pulse_async_single_duration_var = StringVar(value="150")
        ttk.Entry(async_pulse_frame, textvariable=self.pulse_async_single_duration_var, width=10).pack(side=LEFT, padx=5)
        
        ttk.Button(async_pulse_frame, text="Pulse Async", 
                   command=lambda: self.execute_pulseAsync()).pack(side=LEFT, padx=5)
        
        # Multiple pulses (blocking)
        ttk.Label(frame, text="Multiple Pulses (blocking)").pack(anchor=W, padx=10, pady=5)
        multi_frame = ttk.Frame(frame)
        multi_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Label(multi_frame, text="Channel:").pack(side=LEFT, padx=5)
        self.pulse_multi_channel_var = StringVar(value="0")
        ttk.Entry(multi_frame, textvariable=self.pulse_multi_channel_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Label(multi_frame, text="Pulse (ms):").pack(side=LEFT, padx=5)
        self.pulse_width_var = StringVar(value="50")
        ttk.Entry(multi_frame, textvariable=self.pulse_width_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Label(multi_frame, text="Pause (ms):").pack(side=LEFT, padx=5)
        self.pause_width_var = StringVar(value="50")
        ttk.Entry(multi_frame, textvariable=self.pause_width_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Label(multi_frame, text="Count:").pack(side=LEFT, padx=5)
        self.pulse_count_var = StringVar(value="5")
        ttk.Entry(multi_frame, textvariable=self.pulse_count_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Button(multi_frame, text="Generate", 
                   command=lambda: self.execute_generatePulses()).pack(side=LEFT, padx=5)
        
        # Async pulses
        ttk.Label(frame, text="Async Pulses (non-blocking)").pack(anchor=W, padx=10, pady=5)
        async_frame = ttk.Frame(frame)
        async_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Label(async_frame, text="Channel:").pack(side=LEFT, padx=5)
        self.pulse_async_channel_var = StringVar(value="0")
        ttk.Entry(async_frame, textvariable=self.pulse_async_channel_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Label(async_frame, text="Pulse (ms):").pack(side=LEFT, padx=5)
        self.async_pulse_width_var = StringVar(value="100")
        ttk.Entry(async_frame, textvariable=self.async_pulse_width_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Label(async_frame, text="Pause (ms):").pack(side=LEFT, padx=5)
        self.async_pause_width_var = StringVar(value="100")
        ttk.Entry(async_frame, textvariable=self.async_pause_width_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Label(async_frame, text="Count:").pack(side=LEFT, padx=5)
        self.async_pulse_count_var = StringVar(value="3")
        ttk.Entry(async_frame, textvariable=self.async_pulse_count_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Button(async_frame, text="Start Async", 
                   command=lambda: self.execute_generatePulsesAsync()).pack(side=LEFT, padx=5)
        
        # Pulse control
        ttk.Label(frame, text="Pulse Control").pack(anchor=W, padx=10, pady=5)
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Label(control_frame, text="Channel:").pack(side=LEFT, padx=5)
        self.pulse_control_channel_var = StringVar(value="0")
        ttk.Entry(control_frame, textvariable=self.pulse_control_channel_var, width=5).pack(side=LEFT, padx=5)
        
        ttk.Button(control_frame, text="Check Status", 
                   command=lambda: self.execute_isPulsing()).pack(side=LEFT, padx=5)
        
        ttk.Button(control_frame, text="Stop Pulse", 
                   command=lambda: self.execute_stopPulse()).pack(side=LEFT, padx=5)
    
    def setup_raw_tab(self, notebook):
        """Setup Raw command tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Raw Command")
        
        ttk.Label(frame, text="Method:").pack(anchor=W, padx=10, pady=5)
        self.raw_method_var = StringVar()
        ttk.Entry(frame, textvariable=self.raw_method_var, width=30).pack(fill=X, padx=10, pady=5)
        
        ttk.Label(frame, text="Parameters (JSON):").pack(anchor=W, padx=10, pady=5)
        self.raw_params = scrolledtext.ScrolledText(frame, height=6)
        self.raw_params.pack(fill=BOTH, expand=True, padx=10, pady=5)
        self.raw_params.insert("1.0", "{}")
        
        ttk.Button(frame, text="Execute", command=self.execute_raw_command).pack(pady=5)
    
    def on_mode_changed(self, *args):
        """Handle communication mode change"""
        self.comm_mode = COMM_USB if self.mode_var.get() == "USB" else COMM_WIFI
    
    def connect(self):
        """Connect to ESP32"""
        try:
            kwargs = {}
            if self.comm_mode == COMM_USB:
                kwargs['port'] = self.usb_port_var.get()
            else:
                kwargs['host'] = self.wifi_host_var.get()
                try:
                    kwargs['port'] = int(self.wifi_port_var.get())
                except ValueError:
                    kwargs['port'] = CONFIG['wifi_port']
            
            self.client = RPCClient(comm_mode=self.comm_mode, **kwargs)
            success, message = self.client.connect()
            
            if success:
                self.output_message(f"✓ Connected: {message}")
                self.connect_btn.config(state=DISABLED)
                self.disconnect_btn.config(state=NORMAL)
                self.update_connection_status()
            else:
                messagebox.showerror("Connection Error", f"Failed to connect: {message}")
                self.output_message(f"✗ Connection failed: {message}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.output_message(f"✗ Error: {e}")
    
    def disconnect(self):
        """Disconnect from ESP32"""
        if self.client:
            self.client.disconnect()
            self.output_message("✓ Disconnected")
            self.connect_btn.config(state=NORMAL)
            self.disconnect_btn.config(state=DISABLED)
            self.update_connection_status()
    
    def update_connection_status(self):
        """Update connection status label"""
        if self.client and self.client.is_connected():
            self.status_label.config(text="Connected ✓", foreground="green")
        else:
            self.status_label.config(text="Disconnected ✗", foreground="red")
    
    def output_message(self, message):
        """Add message to output"""
        self.output.config(state=NORMAL)
        self.output.insert(END, message + "\n")
        self.output.see(END)
        self.output.config(state=DISABLED)
    
    def clear_output(self):
        """Clear output"""
        self.output.config(state=NORMAL)
        self.output.delete("1.0", END)
        self.output.config(state=DISABLED)
    
    # GPIO Commands
    def execute_gpio_pinmode(self):
        """Execute pinMode"""
        if not self.check_connection():
            return
        
        try:
            pin = int(self.pin_var.get())
            mode = int(self.mode_pin_var.get())
            
            result, msg = self.client.pinMode(pin, mode)
            self.output_message(f"pinMode({pin}, {mode}) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
    
    def execute_digitalWrite(self):
        """Execute digitalWrite"""
        if not self.check_connection():
            return
        
        try:
            pin = int(self.dpin_var.get())
            value = int(self.dvalue_var.get())
            
            result, msg = self.client.digitalWrite(pin, value)
            self.output_message(f"digitalWrite({pin}, {value}) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
    
    def execute_digitalRead(self):
        """Execute digitalRead"""
        if not self.check_connection():
            return
        
        try:
            pin = int(self.read_pin_var.get())
            result, msg, value = self.client.digitalRead(pin)
            self.output_message(f"digitalRead({pin}) -> Code: {result}, Value: {value}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
    
    def execute_analogRead(self):
        """Execute analogRead"""
        if not self.check_connection():
            return
        
        try:
            pin = int(self.aread_pin_var.get())
            result, msg, value = self.client.analogRead(pin)
            self.output_message(f"analogRead({pin}) -> Code: {result}, Value: {value}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
    
    # System Commands
    def execute_delay(self):
        """Execute delay"""
        if not self.check_connection():
            return
        
        try:
            ms = int(self.delay_var.get())
            result, msg = self.client.delay(ms)
            self.output_message(f"delay({ms}) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
    
    def execute_getMillis(self):
        """Execute getMillis"""
        if not self.check_connection():
            return
        
        result, msg, value = self.client.getMillis()
        self.output_message(f"millis() -> Code: {result}, Value: {value}ms, {msg}")
    
    def execute_getFreeMem(self):
        """Execute getFreeMem"""
        if not self.check_connection():
            return
        
        result, msg, value = self.client.getFreeMem()
        self.output_message(f"freeMem() -> Code: {result}, Value: {value} bytes, {msg}")
    
    def execute_getChipID(self):
        """Execute getChipID"""
        if not self.check_connection():
            return
        
        result, msg, value = self.client.getChipID()
        self.output_message(f"chipID() -> Code: {result}, Value: 0x{value:X}, {msg}")
    
    # PWM Commands
    def execute_ledcSetup(self):
        """Execute ledcSetup"""
        if not self.check_connection():
            return
        
        try:
            channel = int(self.pwm_channel_var.get())
            freq = int(self.pwm_freq_var.get())
            bits = int(self.pwm_bits_var.get())
            
            result, msg = self.client.ledcSetup(channel, freq, bits)
            self.output_message(f"ledcSetup({channel}, {freq}, {bits}) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
    
    def execute_ledcWrite(self):
        """Execute ledcWrite"""
        if not self.check_connection():
            return
        
        try:
            channel = int(self.pwm_write_channel_var.get())
            duty = int(self.pwm_duty_var.get())
            
            result, msg = self.client.ledcWrite(channel, duty)
            self.output_message(f"ledcWrite({channel}, {duty}) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
    
    # Pulse Library Commands
    def execute_pulseBegin(self):
        """Execute pulseBegin"""
        if not self.check_connection():
            return
        
        try:
            channel = int(self.pulse_channel_var.get())
            pin = int(self.pulse_pin_var.get())
            
            result, msg = self.client.pulseBegin(channel, pin)
            self.output_message(f"pulseBegin({channel}, {pin}) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
    
    def execute_pulse(self):
        """Execute pulse"""
        if not self.check_connection():
            return
        
        try:
            channel = int(self.pulse_single_channel_var.get())
            duration = int(self.pulse_duration_var.get())
            
            result, msg = self.client.pulse(channel, duration)
            self.output_message(f"pulse({channel}, {duration}ms) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
    
    def execute_pulseAsync(self):
        """Execute pulseAsync"""
        if not self.check_connection():
            return
        
        try:
            channel = int(self.pulse_async_single_channel_var.get())
            duration = int(self.pulse_async_single_duration_var.get())
            
            result, msg = self.client.pulseAsync(channel, duration)
            self.output_message(f"pulseAsync({channel}, {duration}ms) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
    
    def execute_generatePulses(self):
        """Execute generatePulses"""
        if not self.check_connection():
            return
        
        try:
            channel = int(self.pulse_multi_channel_var.get())
            pulse_width = int(self.pulse_width_var.get())
            pause_width = int(self.pause_width_var.get())
            count = int(self.pulse_count_var.get())
            
            result, msg = self.client.generatePulses(channel, pulse_width, pause_width, count)
            self.output_message(f"generatePulses({channel}, {pulse_width}, {pause_width}, {count}) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
    
    def execute_generatePulsesAsync(self):
        """Execute generatePulsesAsync"""
        if not self.check_connection():
            return
        
        try:
            channel = int(self.pulse_async_channel_var.get())
            pulse_width = int(self.async_pulse_width_var.get())
            pause_width = int(self.async_pause_width_var.get())
            count = int(self.async_pulse_count_var.get())
            
            result, msg = self.client.generatePulsesAsync(channel, pulse_width, pause_width, count)
            self.output_message(f"generatePulsesAsync({channel}, {pulse_width}, {pause_width}, {count}) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
    
    def execute_isPulsing(self):
        """Execute isPulsing"""
        if not self.check_connection():
            return
        
        try:
            channel = int(self.pulse_control_channel_var.get())
            result, msg, pulsing = self.client.isPulsing(channel)
            status = "ACTIVE" if pulsing else "IDLE"
            self.output_message(f"isPulsing({channel}) -> Code: {result}, Status: {status}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
    
    def execute_stopPulse(self):
        """Execute stopPulse"""
        if not self.check_connection():
            return
        
        try:
            channel = int(self.pulse_control_channel_var.get())
            result, msg = self.client.stopPulse(channel)
            self.output_message(f"stopPulse({channel}) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
    
    # Raw Command
    def execute_raw_command(self):
        """Execute raw command"""
        if not self.check_connection():
            return
        
        try:
            method = self.raw_method_var.get()
            params_str = self.raw_params.get("1.0", END)
            params = json.loads(params_str) if params_str.strip() else {}
            
            result, msg, data = self.client.call_raw(method, params)
            output = f"call_raw('{method}', {params}) -> Code: {result}, {msg}"
            if data:
                output += f"\nData: {json.dumps(data, indent=2)}"
            self.output_message(output)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON in parameters")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def check_connection(self):
        """Check if connected"""
        if not self.client or not self.client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return False
        return True


if __name__ == "__main__":
    root = Tk()
    app = RPCTestGUI(root)
    root.mainloop()
