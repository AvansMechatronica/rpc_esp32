"""
Tab for DAC (Digital-to-Analog Converter) functions in ESP32 RPC GUI
"""


from tkinter import *
from tkinter import ttk, messagebox


class DACTab:
    def __init__(self, notebook, parent):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="DAC")
        self.parent = parent
        self.setup_dac_tab()

    def setup_dac_tab(self):
        frame = self.frame
        
        # dacSetVoltage - Set voltage on single channel
        ttk.Label(frame, text="dacSetVoltage - Set Single Channel", font=("Arial", 10, "bold")).pack(anchor=W, padx=10, pady=10)
        set_frame = ttk.Frame(frame)
        set_frame.pack(fill=X, padx=10, pady=5)

        ttk.Label(set_frame, text="Channel:").pack(side=LEFT, padx=5)
        self.dac_channel_var = StringVar(value="0")
        channel_combo = ttk.Combobox(set_frame, textvariable=self.dac_channel_var, 
                                     values=["0", "1", "2", "3"], state="readonly", width=5)
        channel_combo.pack(side=LEFT, padx=5)
        
        ttk.Label(set_frame, text="Voltage (V):").pack(side=LEFT, padx=5)
        self.dac_voltage_var = StringVar(value="2.5")
        ttk.Entry(set_frame, textvariable=self.dac_voltage_var, width=10).pack(side=LEFT, padx=5)

        ttk.Button(set_frame, text="Set Voltage", 
                   command=self.execute_dacSetVoltage).pack(side=LEFT, padx=5)

        # dacSetVoltageAll - Set voltage on all channels
        ttk.Label(frame, text="dacSetVoltageAll - Set All Channels", font=("Arial", 10, "bold")).pack(anchor=W, padx=10, pady=10)
        set_all_frame = ttk.Frame(frame)
        set_all_frame.pack(fill=X, padx=10, pady=5)

        ttk.Label(set_all_frame, text="Voltage (V):").pack(side=LEFT, padx=5)
        self.dac_voltage_all_var = StringVar(value="2.5")
        ttk.Entry(set_all_frame, textvariable=self.dac_voltage_all_var, width=10).pack(side=LEFT, padx=5)

        ttk.Button(set_all_frame, text="Set All", 
                   command=self.execute_dacSetVoltageAll).pack(side=LEFT, padx=5)

        # Common voltage presets
        ttk.Label(frame, text="Quick Presets", font=("Arial", 10, "bold")).pack(anchor=W, padx=10, pady=10)
        presets_frame = ttk.Frame(frame)
        presets_frame.pack(fill=X, padx=10, pady=5)

        # Preset buttons
        presets = [("0V", 0.0), ("1.25V", 1.25), ("2.5V", 2.5), ("3.75V", 3.75), ("5V", 5.0)]
        for label, voltage in presets:
            ttk.Button(presets_frame, text=label, 
                       command=lambda v=voltage: self.set_preset(v)).pack(side=LEFT, padx=3)

    def execute_dacSetVoltage(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            channel = int(self.dac_channel_var.get())
            voltage = float(self.dac_voltage_var.get())
            
            # Use raw call to see actual response
            result, msg, data = client.call_raw("dacSetVoltage", {"channel": channel, "voltage": voltage})
            self.parent.output_message(f"[DEBUG] Raw response: result={result}, msg={msg}, data={data}")
            self.parent.output_message(f"dacSetVoltage({channel}, {voltage}V) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values. Channel must be 0-3, Voltage must be a number")

    def execute_dacSetVoltageAll(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            voltage = float(self.dac_voltage_all_var.get())
            result, msg = client.dacSetVoltageAll(voltage)
            self.parent.output_message(f"dacSetVoltageAll({voltage}V) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Voltage must be a number")

    def set_preset(self, voltage):
        """Set voltage from preset button"""
        self.dac_voltage_all_var.set(str(voltage))
        self.execute_dacSetVoltageAll()
