"""
Tab for DIO (Digital I/O) functions in ESP32 RPC GUI
"""


from tkinter import *
from tkinter import ttk, messagebox


class DIOTab:
    def __init__(self, notebook, parent):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="DIO")
        self.parent = parent
        self.setup_dio_tab()

    def _extract_value(self, data, preferred_keys=None):
        """Helper to extract value from response data"""
        if isinstance(data, dict):
            if preferred_keys:
                for key in preferred_keys:
                    if key in data:
                        return data[key]
            if len(data) == 1:
                return next(iter(data.values()))
        return data

    def setup_dio_tab(self):
        frame = self.frame
        
        # dioGetInput - Read all 8 input bits
        ttk.Label(frame, text="dioGetInput - Read All Inputs", font=("Arial", 10, "bold")).pack(anchor=W, padx=10, pady=10)
        get_input_frame = ttk.Frame(frame)
        get_input_frame.pack(fill=X, padx=10, pady=5)

        ttk.Button(get_input_frame, text="Read Inputs", 
                   command=self.execute_dioGetInput).pack(side=LEFT, padx=5)
        
        self.input_value_var = StringVar(value="-")
        ttk.Label(get_input_frame, text="Value (8-bit):").pack(side=LEFT, padx=5)
        ttk.Label(get_input_frame, textvariable=self.input_value_var, font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        
        self.input_binary_var = StringVar(value="-")
        ttk.Label(get_input_frame, text="Binary:").pack(side=LEFT, padx=5)
        ttk.Label(get_input_frame, textvariable=self.input_binary_var, font=("Courier", 9)).pack(side=LEFT, padx=5)

        ttk.Separator(frame, orient=HORIZONTAL).pack(fill=X, padx=10, pady=10)

        # dioIsBitSet - Check if specific bit is set
        ttk.Label(frame, text="dioIsBitSet - Check Specific Bit", font=("Arial", 10, "bold")).pack(anchor=W, padx=10, pady=10)
        is_bit_set_frame = ttk.Frame(frame)
        is_bit_set_frame.pack(fill=X, padx=10, pady=5)

        ttk.Label(is_bit_set_frame, text="Bit Number (0-5):").pack(side=LEFT, padx=5)
        self.check_bit_var = StringVar(value="0")
        ttk.Combobox(is_bit_set_frame, textvariable=self.check_bit_var, 
                     values=["0", "1", "2", "3", "4", "5"], 
                     state="readonly", width=5).pack(side=LEFT, padx=5)

        ttk.Button(is_bit_set_frame, text="Check Bit", 
                   command=self.execute_dioIsBitSet).pack(side=LEFT, padx=5)
        
        self.bit_status_var = StringVar(value="-")
        ttk.Label(is_bit_set_frame, text="Status:").pack(side=LEFT, padx=5)
        ttk.Label(is_bit_set_frame, textvariable=self.bit_status_var, font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)

        ttk.Separator(frame, orient=HORIZONTAL).pack(fill=X, padx=10, pady=10)

        # dioSetOutput - Set all 8 output bits
        ttk.Label(frame, text="dioSetOutput - Write All Outputs", font=("Arial", 10, "bold")).pack(anchor=W, padx=10, pady=10)
        set_output_frame = ttk.Frame(frame)
        set_output_frame.pack(fill=X, padx=10, pady=5)

        ttk.Label(set_output_frame, text="Value (0-255):").pack(side=LEFT, padx=5)
        self.output_value_var = StringVar(value="0")
        ttk.Entry(set_output_frame, textvariable=self.output_value_var, width=10).pack(side=LEFT, padx=5)

        ttk.Button(set_output_frame, text="Set Outputs", 
                   command=self.execute_dioSetOutput).pack(side=LEFT, padx=5)

        # Quick presets for output
        presets_frame = ttk.Frame(frame)
        presets_frame.pack(fill=X, padx=10, pady=5)
        ttk.Label(presets_frame, text="Quick Presets:").pack(side=LEFT, padx=5)
        
        presets = [("All Off (0)", 0), ("All On (255)", 255), ("0x55 (85)", 85), ("0xAA (170)", 170)]
        for label, value in presets:
            ttk.Button(presets_frame, text=label, 
                       command=lambda v=value: self.set_output_preset(v)).pack(side=LEFT, padx=3)

        ttk.Separator(frame, orient=HORIZONTAL).pack(fill=X, padx=10, pady=10)

        # Bit Manipulation - Set/Clear/Toggle individual bits
        ttk.Label(frame, text="Bit Manipulation - Set/Clear/Toggle", font=("Arial", 10, "bold")).pack(anchor=W, padx=10, pady=10)
        
        bit_manip_frame = ttk.Frame(frame)
        bit_manip_frame.pack(fill=X, padx=10, pady=5)

        ttk.Label(bit_manip_frame, text="Bit Number (0-5):").pack(side=LEFT, padx=5)
        self.bit_manip_num_var = StringVar(value="0")
        ttk.Combobox(bit_manip_frame, textvariable=self.bit_manip_num_var, 
                     values=["0", "1", "2", "3", "4", "5"], 
                     state="readonly", width=5).pack(side=LEFT, padx=5)

        ttk.Button(bit_manip_frame, text="Set Bit (1)", 
                   command=self.execute_dioSetBit).pack(side=LEFT, padx=5)
        
        ttk.Button(bit_manip_frame, text="Clear Bit (0)", 
                   command=self.execute_dioClearBit).pack(side=LEFT, padx=5)
        
        ttk.Button(bit_manip_frame, text="Toggle Bit", 
                   command=self.execute_dioToggleBit).pack(side=LEFT, padx=5)

    def execute_dioGetInput(self):
        """Call dioGetInput RPC function"""
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            result, msg, value = client.dioGetInput()
            
            # Display as decimal and binary
            self.input_value_var.set(f"{value}")
            self.input_binary_var.set(f"{value:08b}")
            
            self.parent.output_message(f"dioGetInput() -> Code: {result}, Value: {value} (0b{value:08b}), {msg}")
        except Exception as e:
            self.parent.output_message(f"[ERROR] {str(e)}")

    def execute_dioIsBitSet(self):
        """Call dioIsBitSet RPC function"""
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            bit_number = int(self.check_bit_var.get())
            
            result, msg, bit_set = client.dioIsBitSet(bit_number)
            
            status = "SET (1)" if bit_set else "CLEAR (0)"
            self.bit_status_var.set(status)
            
            self.parent.output_message(f"dioIsBitSet({bit_number}) -> Code: {result}, Status: {status}, {msg}")
        except Exception as e:
            self.parent.output_message(f"[ERROR] {str(e)}")

    def execute_dioSetOutput(self):
        """Call dioSetOutput RPC function"""
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            value = int(self.output_value_var.get())
            
            if value < 0 or value > 255:
                messagebox.showerror("Error", "Value must be between 0 and 255")
                return
            
            result, msg = client.dioSetOutput(value)
            self.parent.output_message(f"dioSetOutput({value}) -> Code: {result}, Binary: 0b{value:08b}, {msg}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Value must be an integer (0-255)")
        except Exception as e:
            self.parent.output_message(f"[ERROR] {str(e)}")

    def execute_dioSetBit(self):
        """Call dioSetBit RPC function - Sets bit to 1"""
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            bit_number = int(self.bit_manip_num_var.get())
            
            result, msg = client.dioSetBit(bit_number)
            self.parent.output_message(f"dioSetBit({bit_number}) -> Code: {result}, {msg}")
        except Exception as e:
            self.parent.output_message(f"[ERROR] {str(e)}")

    def execute_dioClearBit(self):
        """Call dioClearBit RPC function - Clears bit to 0"""
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            bit_number = int(self.bit_manip_num_var.get())
            
            result, msg = client.dioClearBit(bit_number)
            self.parent.output_message(f"dioClearBit({bit_number}) -> Code: {result}, {msg}")
        except Exception as e:
            self.parent.output_message(f"[ERROR] {str(e)}")

    def execute_dioToggleBit(self):
        """Call dioToggleBit RPC function - Toggles bit state"""
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return
        try:
            bit_number = int(self.bit_manip_num_var.get())
            
            result, msg = client.dioToggleBit(bit_number)
            self.parent.output_message(f"dioToggleBit({bit_number}) -> Code: {result}, {msg}")
        except Exception as e:
            self.parent.output_message(f"[ERROR] {str(e)}")

    def set_output_preset(self, value):
        """Set output value from preset button"""
        self.output_value_var.set(str(value))
        self.execute_dioSetOutput()
