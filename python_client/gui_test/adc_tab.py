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

    def _extract_value(self, data, preferred_keys=None):
        if isinstance(data, dict):
            if preferred_keys:
                for key in preferred_keys:
                    if key in data:
                        return data[key]
            if len(data) == 1:
                return next(iter(data.values()))
        return data

    def read_raw(self):
        """Call adcReadRaw RPC function"""
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            channel = int(self.raw_channel_var.get())
            average_count = int(self.raw_average_var.get())
            
            result, msg, value = client.adcReadRaw(channel, averageCount=average_count)
            self.raw_value_var.set(f"{value}")
            self.parent.output_message(f"adcReadRaw({channel}, {average_count}) -> Code: {result}, Value: {value}, {msg}")
        except Exception as e:
            self.parent.output_message(f"[ERROR] {str(e)}")
    
    def read_voltage(self):
        """Call adcReadVoltage RPC function"""
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            channel = int(self.voltage_channel_var.get())
            average_count = int(self.voltage_average_var.get())
            
            result, msg, value = client.adcReadVoltage(channel, averageCount=average_count)
            self.voltage_value_var.set(f"{value} V")
            self.parent.output_message(f"adcReadVoltage({channel}, {average_count}) -> Code: {result}, Value: {value}V, {msg}")
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
            
            result, msg, pressed = client.isButtonPressed(button)
            status = "PRESSED" if pressed else "NOT PRESSED"
            self.button_status_var.set(status)
            self.parent.output_message(f"isButtonPressed({button}) -> Code: {result}, Status: {status}, {msg}")
        except Exception as e:
            self.parent.output_message(f"[ERROR] {str(e)}")

    def setup_adc_tab(self):
        frame = self.frame
        # adcReadRaw
        ttk.Label(frame, text="adcReadRaw", font=("Arial", 10, "bold")).pack(anchor=W, padx=10, pady=10)
        raw_frame = ttk.Frame(frame)
        raw_frame.pack(fill=X, padx=10, pady=5)

        ttk.Label(raw_frame, text="Channel:").pack(side=LEFT, padx=5)
        self.raw_channel_var = StringVar(value="0")
        ttk.Combobox(raw_frame, textvariable=self.raw_channel_var, values=("0", "1", "2", "3", "4", "5"), width=5, state="readonly").pack(side=LEFT, padx=5)

        ttk.Label(raw_frame, text="Average Count:").pack(side=LEFT, padx=5)
        self.raw_average_var = StringVar(value="1")
        ttk.Entry(raw_frame, textvariable=self.raw_average_var, width=5).pack(side=LEFT, padx=5)

        ttk.Button(raw_frame, text="Read Raw", 
                   command=self.read_raw).pack(side=LEFT, padx=5)

        self.raw_value_var = StringVar(value="-")
        ttk.Label(raw_frame, text="Value:").pack(side=LEFT, padx=5)
        ttk.Label(raw_frame, textvariable=self.raw_value_var).pack(side=LEFT, padx=5)

        ttk.Separator(frame, orient=HORIZONTAL).pack(fill=X, padx=10, pady=10)

        # adcReadVoltage
        ttk.Label(frame, text="adcReadVoltage", font=("Arial", 10, "bold")).pack(anchor=W, padx=10, pady=10)
        voltage_frame = ttk.Frame(frame)
        voltage_frame.pack(fill=X, padx=10, pady=5)

        ttk.Label(voltage_frame, text="Channel:").pack(side=LEFT, padx=5)
        self.voltage_channel_var = StringVar(value="0")
        ttk.Combobox(voltage_frame, textvariable=self.voltage_channel_var, values=("0", "1", "2", "3", "4", "5"), width=5, state="readonly").pack(side=LEFT, padx=5)

        ttk.Label(voltage_frame, text="Average Count:").pack(side=LEFT, padx=5)
        self.voltage_average_var = StringVar(value="1")
        ttk.Entry(voltage_frame, textvariable=self.voltage_average_var, width=5).pack(side=LEFT, padx=5)

        ttk.Button(voltage_frame, text="Read Voltage", 
                   command=self.read_voltage).pack(side=LEFT, padx=5)

        self.voltage_value_var = StringVar(value="-")
        ttk.Label(voltage_frame, text="Value:").pack(side=LEFT, padx=5)
        ttk.Label(voltage_frame, textvariable=self.voltage_value_var).pack(side=LEFT, padx=5)

        ttk.Separator(frame, orient=HORIZONTAL).pack(fill=X, padx=10, pady=10)

        # isButtonPressed
        ttk.Label(frame, text="isButtonPressed", font=("Arial", 10, "bold")).pack(anchor=W, padx=10, pady=10)
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=X, padx=10, pady=5)

        ttk.Label(button_frame, text="Analog Button:").pack(side=LEFT, padx=5)
        self.button_channel_var = StringVar(value="1")
        ttk.Combobox(button_frame, textvariable=self.button_channel_var, values=("1", "2"), width=5, state="readonly").pack(side=LEFT, padx=5)

        ttk.Button(button_frame, text="Check Button", 
                   command=self.is_button_pressed).pack(side=LEFT, padx=5)

        self.button_status_var = StringVar(value="-")
        ttk.Label(button_frame, text="Status:").pack(side=LEFT, padx=5)
        ttk.Label(button_frame, textvariable=self.button_status_var).pack(side=LEFT, padx=5)
