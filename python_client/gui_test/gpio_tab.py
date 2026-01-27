"""
Tab for GPIO functions in ESP32 RPC GUI
"""

from tkinter import *
from tkinter import ttk


class GPIOTab:
    def __init__(self, notebook, parent):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="GPIO")
        self.parent = parent
        self.setup_gpio_tab()

    def execute_gpio_pinmode(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            pin = int(self.pin_var.get())
            mode = int(self.mode_pin_var.get())
            result, msg = client.pinMode(pin, mode)
            self.parent.output_message(f"pinMode({pin}, {mode}) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def execute_digitalWrite(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            pin = int(self.dpin_var.get())
            value = int(self.dvalue_var.get())
            result, msg = client.digitalWrite(pin, value)
            self.parent.output_message(f"digitalWrite({pin}, {value}) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def execute_digitalRead(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            pin = int(self.read_pin_var.get())
            result, msg, value = client.digitalRead(pin)
            self.parent.output_message(f"digitalRead({pin}) -> Code: {result}, Value: {value}, {msg}")
            if hasattr(self, 'digital_read_value_label'):
                if result == 0 and value is not None:
                    self.digital_read_value_label.config(text=f"Value: {value}")
                else:
                    self.digital_read_value_label.config(text="Value: -")
                self.digital_read_value_label.update()
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def execute_analogRead(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            pin = int(self.aread_pin_var.get())
            result, msg, value = client.analogRead(pin)
            self.parent.output_message(f"analogRead({pin}) -> Code: {result}, Value: {value}, {msg}")
            if hasattr(self, 'analog_read_value_label'):
                if result == 0 and value is not None:
                    self.analog_read_value_label.config(text=f"Value: {value}")
                else:
                    self.analog_read_value_label.config(text="Value: -")
                self.analog_read_value_label.update()
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def setup_gpio_tab(self):
        frame = self.frame
        # pinMode
        ttk.Label(frame, text="pinMode").pack(anchor=W, padx=10, pady=5)
        gpio_frame = ttk.Frame(frame)
        gpio_frame.pack(fill=X, padx=10, pady=5)

        ttk.Label(gpio_frame, text="Pin:").pack(side=LEFT, padx=5)
        self.pin_var = StringVar(value="2")
        ttk.Entry(gpio_frame, textvariable=self.pin_var, width=5).pack(side=LEFT, padx=5)

        ttk.Label(gpio_frame, text="Mode (0=IN, 1=OUT, 2=PULLUP):").pack(side=LEFT, padx=5)
        self.mode_pin_var = StringVar(value="1")
        ttk.Entry(gpio_frame, textvariable=self.mode_pin_var, width=5).pack(side=LEFT, padx=5)

        ttk.Button(gpio_frame, text="pinMode", 
               command=self.execute_gpio_pinmode).pack(side=LEFT, padx=5)

        # digitalWrite
        ttk.Label(frame, text="digitalWrite").pack(anchor=W, padx=10, pady=5)
        dig_frame = ttk.Frame(frame)
        dig_frame.pack(fill=X, padx=10, pady=5)

        ttk.Label(dig_frame, text="Pin:").pack(side=LEFT, padx=5)
        self.dpin_var = StringVar(value="2")
        ttk.Entry(dig_frame, textvariable=self.dpin_var, width=5).pack(side=LEFT, padx=5)

        ttk.Label(dig_frame, text="Value (0 or 1):").pack(side=LEFT, padx=5)
        self.dvalue_var = StringVar(value="1")
        ttk.Entry(dig_frame, textvariable=self.dvalue_var, width=5).pack(side=LEFT, padx=5)

        ttk.Button(dig_frame, text="digitalWrite", 
               command=self.execute_digitalWrite).pack(side=LEFT, padx=5)

        # digitalRead
        ttk.Label(frame, text="digitalRead").pack(anchor=W, padx=10, pady=5)
        read_frame = ttk.Frame(frame)
        read_frame.pack(fill=X, padx=10, pady=5)

        ttk.Label(read_frame, text="Pin:").pack(side=LEFT, padx=5)
        self.read_pin_var = StringVar(value="2")
        ttk.Entry(read_frame, textvariable=self.read_pin_var, width=5).pack(side=LEFT, padx=5)

        ttk.Button(read_frame, text="digitalRead", 
               command=self.execute_digitalRead).pack(side=LEFT, padx=5)
        self.digital_read_value_label = ttk.Label(read_frame, text="Value: -")
        self.digital_read_value_label.pack(side=LEFT, padx=5)

        # analogRead
        ttk.Label(frame, text="analogRead").pack(anchor=W, padx=10, pady=5)
        aread_frame = ttk.Frame(frame)
        aread_frame.pack(fill=X, padx=10, pady=5)

        ttk.Label(aread_frame, text="Pin:").pack(side=LEFT, padx=5)
        self.aread_pin_var = StringVar(value="36")
        ttk.Entry(aread_frame, textvariable=self.aread_pin_var, width=5).pack(side=LEFT, padx=5)

        ttk.Button(aread_frame, text="analogRead", 
               command=self.execute_analogRead).pack(side=LEFT, padx=5)
        self.analog_read_value_label = ttk.Label(aread_frame, text="Value: -")
        self.analog_read_value_label.pack(side=LEFT, padx=5)
