"""
Tab for Pulse Library functions in ESP32 RPC GUI
"""


from tkinter import *
from tkinter import ttk, messagebox


class PulseTab:
    def __init__(self, notebook, parent):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Pulse Library")
        self.parent = parent
        self.setup_pulse_tab()

    def execute_pulseBegin(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            channel = int(self.pulse_channel_var.get())
            pin = int(self.pulse_pin_var.get())
            result, msg = client.pulseBegin(channel, pin)
            self.parent.output_message(f"pulseBegin({channel}, {pin}) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def execute_pulse(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            channel = int(self.pulse_single_channel_var.get())
            duration = int(self.pulse_duration_var.get())
            result, msg = client.pulse(channel, duration)
            self.parent.output_message(f"pulse({channel}, {duration}ms) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def execute_pulseAsync(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            channel = int(self.pulse_async_single_channel_var.get())
            duration = int(self.pulse_async_single_duration_var.get())
            result, msg = client.pulseAsync(channel, duration)
            self.parent.output_message(f"pulseAsync({channel}, {duration}ms) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def execute_generatePulses(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            channel = int(self.pulse_multi_channel_var.get())
            pulse_width = int(self.pulse_width_var.get())
            pause_width = int(self.pause_width_var.get())
            count = int(self.pulse_count_var.get())
            result, msg = client.generatePulses(channel, pulse_width, pause_width, count)
            self.parent.output_message(f"generatePulses({channel}, {pulse_width}, {pause_width}, {count}) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def execute_generatePulsesAsync(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            channel = int(self.pulse_async_channel_var.get())
            pulse_width = int(self.async_pulse_width_var.get())
            pause_width = int(self.async_pause_width_var.get())
            count = int(self.async_pulse_count_var.get())
            result, msg = client.generatePulsesAsync(channel, pulse_width, pause_width, count)
            self.parent.output_message(f"generatePulsesAsync({channel}, {pulse_width}, {pause_width}, {count}) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def execute_isPulsing(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            channel = int(self.pulse_control_channel_var.get())
            result, msg, pulsing = client.isPulsing(channel)
            status = "ACTIVE" if pulsing else "IDLE"
            self.parent.output_message(f"isPulsing({channel}) -> Code: {result}, Status: {status}, {msg}")
            if hasattr(self, 'pulse_status_label'):
                if result == 0 and pulsing is not None:
                    self.pulse_status_label.config(text=f"Status: {status}")
                else:
                    self.pulse_status_label.config(text="Status: -")
                self.pulse_status_label.update()
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def execute_getRemainingPulses(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            channel = int(self.pulse_control_channel_var.get())
            result, msg, remaining = client.getRemainingPulses(channel)
            self.parent.output_message(f"getRemainingPulses({channel}) -> Code: {result}, Remaining: {remaining}, {msg}")
            if hasattr(self, 'remaining_label'):
                if result == 0 and remaining is not None:
                    self.remaining_label.config(text=f"Remaining: {remaining}")
                else:
                    self.remaining_label.config(text="Remaining: -")
                self.remaining_label.update()
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def execute_stopPulse(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            channel = int(self.pulse_control_channel_var.get())
            result, msg = client.stopPulse(channel)
            self.parent.output_message(f"stopPulse({channel}) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def setup_pulse_tab(self):
        frame = self.frame
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
               command=self.execute_pulseBegin).pack(side=LEFT, padx=5)

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
               command=self.execute_pulse).pack(side=LEFT, padx=5)

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
               command=self.execute_pulseAsync).pack(side=LEFT, padx=5)

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
               command=self.execute_generatePulses).pack(side=LEFT, padx=5)

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
               command=self.execute_generatePulsesAsync).pack(side=LEFT, padx=5)

        # Pulse control
        ttk.Label(frame, text="Pulse Control").pack(anchor=W, padx=10, pady=5)
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=X, padx=10, pady=5)

        row1 = ttk.Frame(control_frame)
        row1.pack(fill=X, padx=5, pady=5)
        ttk.Label(row1, text="Channel:").pack(side=LEFT, padx=5)
        self.pulse_control_channel_var = StringVar(value="0")
        ttk.Entry(row1, textvariable=self.pulse_control_channel_var, width=5).pack(side=LEFT, padx=5)
        ttk.Button(row1, text="Check Status", 
                   command=self.execute_isPulsing).pack(side=LEFT, padx=5)
        self.pulse_status_label = ttk.Label(row1, text="Status: -")
        self.pulse_status_label.pack(side=LEFT, padx=5)

        row2 = ttk.Frame(control_frame)
        row2.pack(fill=X, padx=5, pady=5)
        ttk.Button(row2, text="Remaining Pulses", 
                command=self.execute_getRemainingPulses).pack(side=LEFT, padx=5)
        self.remaining_label = ttk.Label(row2, text="Remaining: -")
        self.remaining_label.pack(side=LEFT, padx=5)

        row3 = ttk.Frame(control_frame)
        row3.pack(fill=X, padx=5, pady=5)
        ttk.Button(row3, text="Stop Pulse", 
                command=self.execute_stopPulse).pack(side=LEFT, padx=5)
