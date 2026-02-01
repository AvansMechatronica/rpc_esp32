"""
Tab for ADC functions in ESP32 RPC GUI
"""


from tkinter import *
from tkinter import ttk, messagebox


class ADCTab:
    def __init__(self, notebook, parent):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="ADC")
        self.parent = parent
        self.setup_adc_tab()

    def read_raw(self):
        """Call ReadRaw RPC function"""
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            channel = int(self.raw_channel_var.get())
            average_count = int(self.raw_average_var.get())
            
            result, msg, data = client.call_raw("ADC.ReadRaw", {"channel": channel, "averageCount": average_count})
            self.parent.output_message(f"ADC.ReadRaw({channel}, {average_count}) -> Code: {result}, Value: {data}, {msg}")
        except Exception as e:
            self.parent.output_message(f"[ERROR] {str(e)}")
    
    def read_voltage(self):
        """Call ReadVoltage RPC function"""
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            channel = int(self.voltage_channel_var.get())
            average_count = int(self.voltage_average_var.get())
            
            result, msg, data = client.call_raw("ADC.ReadVoltage", {"channel": channel, "averageCount": average_count})
            self.parent.output_message(f"ADC.ReadVoltage({channel}, {average_count}) -> Code: {result}, Value: {data}V, {msg}")
        except Exception as e:
            self.parent.output_message(f"[ERROR] {str(e)}")
    
    def is_button_pressed(self):
        """Call IsButtonPressed RPC function"""
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            button = int(self.button_channel_var.get())
            
            result, msg, data = client.call_raw("ADC.IsButtonPressed", {"analogButton": button})
            status = "PRESSED" if data else "NOT PRESSED"
            self.parent.output_message(f"ADC.IsButtonPressed({button}) -> Code: {result}, Status: {status}, {msg}")
        except Exception as e:
            self.parent.output_message(f"[ERROR] {str(e)}")

    def setup_adc_tab(self):
        frame = self.frame
        # ReadRaw
        ttk.Label(frame, text="ADC.ReadRaw").pack(anchor=W, padx=10, pady=5)
        raw_frame = ttk.Frame(frame)
        raw_frame.pack(fill=X, padx=10, pady=5)

        ttk.Label(raw_frame, text="Channel:").pack(side=LEFT, padx=5)
        self.raw_channel_var = StringVar(value="0")
        ttk.Entry(raw_frame, textvariable=self.raw_channel_var, width=5).pack(side=LEFT, padx=5)

        ttk.Label(raw_frame, text="Average Count:").pack(side=LEFT, padx=5)
        self.raw_average_var = StringVar(value="1")
        ttk.Entry(raw_frame, textvariable=self.raw_average_var, width=5).pack(side=LEFT, padx=5)

        ttk.Button(raw_frame, text="Read Raw", 
                   command=self.read_raw).pack(side=LEFT, padx=5)

        # ReadVoltage
        ttk.Label(frame, text="ADC.ReadVoltage").pack(anchor=W, padx=10, pady=5)
        voltage_frame = ttk.Frame(frame)
        voltage_frame.pack(fill=X, padx=10, pady=5)

        ttk.Label(voltage_frame, text="Channel:").pack(side=LEFT, padx=5)
        self.voltage_channel_var = StringVar(value="0")
        ttk.Entry(voltage_frame, textvariable=self.voltage_channel_var, width=5).pack(side=LEFT, padx=5)

        ttk.Label(voltage_frame, text="Average Count:").pack(side=LEFT, padx=5)
        self.voltage_average_var = StringVar(value="1")
        ttk.Entry(voltage_frame, textvariable=self.voltage_average_var, width=5).pack(side=LEFT, padx=5)

        ttk.Button(voltage_frame, text="Read Voltage", 
                   command=self.read_voltage).pack(side=LEFT, padx=5)

        # IsButtonPressed
        ttk.Label(frame, text="ADC.IsButtonPressed").pack(anchor=W, padx=10, pady=5)
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=X, padx=10, pady=5)

        ttk.Label(button_frame, text="Analog Button:").pack(side=LEFT, padx=5)
        self.button_channel_var = StringVar(value="0")
        ttk.Entry(button_frame, textvariable=self.button_channel_var, width=5).pack(side=LEFT, padx=5)

        ttk.Button(button_frame, text="Check Button", 
                   command=self.is_button_pressed).pack(side=LEFT, padx=5)
