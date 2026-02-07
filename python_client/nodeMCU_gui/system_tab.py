"""
Tab for System functions in ESP32 RPC GUI
"""


from tkinter import *
from tkinter import ttk, messagebox


class SystemTab:
    def __init__(self, notebook, parent):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="System")
        self.parent = parent
        self.setup_system_tab()

    def setup_system_tab(self):
        frame = self.frame
        # delay
        ttk.Label(frame, text="delay (ms)", font=("Arial", 10, "bold")).pack(anchor=W, padx=10, pady=10)
        delay_frame = ttk.Frame(frame)
        delay_frame.pack(fill=X, padx=10, pady=5)

        ttk.Label(delay_frame, text="Milliseconds:").pack(side=LEFT, padx=5)
        self.delay_var = StringVar(value="1000")
        ttk.Entry(delay_frame, textvariable=self.delay_var, width=10).pack(side=LEFT, padx=5)

        ttk.Button(delay_frame, text="delay", 
                   command=self.execute_delay).pack(side=LEFT, padx=5)

        ttk.Separator(frame, orient=HORIZONTAL).pack(fill=X, padx=10, pady=10)

        # getMillis
        ttk.Label(frame, text="System Information", font=("Arial", 10, "bold")).pack(anchor=W, padx=10, pady=10)
        info_frame = ttk.Frame(frame)
        info_frame.pack(fill=X, padx=10, pady=5)

        ttk.Button(info_frame, text="Get Millis", 
                   command=self.execute_getMillis).pack(side=LEFT, padx=5)

        ttk.Button(info_frame, text="Get Free Memory", 
                   command=self.execute_getFreeMem).pack(side=LEFT, padx=5)

        ttk.Button(info_frame, text="Get Chip ID", 
                   command=self.execute_getChipID).pack(side=LEFT, padx=5)

        # System info result labels
        result_frame = ttk.Frame(frame)
        result_frame.pack(fill=X, padx=10, pady=5)

        self.millis_label_var = StringVar(value="Millis: -")
        ttk.Label(result_frame, textvariable=self.millis_label_var).pack(anchor=W, pady=2)

        self.free_mem_label_var = StringVar(value="Free Memory: -")
        ttk.Label(result_frame, textvariable=self.free_mem_label_var).pack(anchor=W, pady=2)

        self.chip_id_label_var = StringVar(value="Chip ID: -")
        ttk.Label(result_frame, textvariable=self.chip_id_label_var).pack(anchor=W, pady=2)

    def execute_delay(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            ms = int(self.delay_var.get())
            result, msg = client.delay(ms)
            self.parent.output_message(f"delay({ms}) -> Code: {result}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def execute_getMillis(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            result, msg, value = client.getMillis()
            if result == 0 and value is not None:
                self.millis_label_var.set(f"Millis: {value} ms")
                self.parent.output_message(f"millis() -> Code: {result}, Value: {value}ms, {msg}")
            else:
                self.millis_label_var.set("Millis: -")
                self.parent.output_message(f"millis() -> Code: {result}, {msg} (No result)")
        except Exception as e:
            self.millis_label_var.set("Millis: -")
            self.parent.output_message(f"millis() -> Error: {str(e)}")

    def execute_getFreeMem(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            result, msg, value = client.getFreeMem()
            if result == 0 and value is not None:
                self.free_mem_label_var.set(f"Free Memory: {value} bytes")
                self.parent.output_message(f"freeMem() -> Code: {result}, Value: {value} bytes, {msg}")
            else:
                self.free_mem_label_var.set("Free Memory: -")
                self.parent.output_message(f"freeMem() -> Code: {result}, {msg} (No result)")
        except Exception as e:
            self.free_mem_label_var.set("Free Memory: -")
            self.parent.output_message(f"freeMem() -> Error: {str(e)}")

    def execute_getChipID(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            result, msg, value = client.getChipID()
            if result == 0 and value is not None:
                self.chip_id_label_var.set(f"Chip ID: 0x{value:X}")
                self.parent.output_message(f"chipID() -> Code: {result}, Value: 0x{value:X}, {msg}")
            else:
                self.chip_id_label_var.set("Chip ID: -")
                self.parent.output_message(f"chipID() -> Code: {result}, {msg} (No result)")
        except Exception as e:
            self.chip_id_label_var.set("Chip ID: -")
            self.parent.output_message(f"chipID() -> Error: {str(e)}")
