"""
Tab for PWM functions in ESP32 RPC GUI
"""


from tkinter import *
from tkinter import ttk, messagebox


class PWMTab:
    def __init__(self, notebook, parent):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="PWM")
        self.parent = parent
        self.setup_pwm_tab()

    def setup_pwm_tab(self):
        frame = self.frame
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
                   command=self.execute_ledcSetup).pack(side=LEFT, padx=5)

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
                   command=self.execute_ledcWrite).pack(side=LEFT, padx=5)

    def execute_ledcSetup(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            channel = int(self.pwm_channel_var.get())
            freq = int(self.pwm_freq_var.get())
            bits = int(self.pwm_bits_var.get())
            result, msg = client.ledcSetup(channel, freq, bits)
            self.parent.output_message(f"ledcSetup({channel}, {freq}, {bits}) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def execute_ledcWrite(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            channel = int(self.pwm_write_channel_var.get())
            duty = int(self.pwm_duty_var.get())
            result, msg = client.ledcWrite(channel, duty)
            self.parent.output_message(f"ledcWrite({channel}, {duty}) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
