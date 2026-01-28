
"""
ESP32 RPC GUI Test Application
Provides interactive GUI for testing RPC functions
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import json

from tkinter import *
from tkinter import ttk, messagebox, scrolledtext
from library.rpc_client import RPCClient
from library.config import COMM_USB, COMM_WIFI, RPC_OK, CONFIG
from gpio_tab import GPIOTab
from system_tab import SystemTab
from pwm_tab import PWMTab
from pulse_tab import PulseTab


class RPCTestGUI:
    """GUI for testing ESP32 RPC functions"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("ESP32 RPC Test Client")
        self.root.geometry("1000x700")
        
        self.client = None
        self.comm_mode = COMM_USB
        self.output_window_visible = False
        
        self.setup_output_window()
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
        self.wifi_host_var = StringVar(value="192.168.2.17")
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

        # Toggle Output Button
        self.toggle_output_btn = ttk.Button(conn_frame, text="Show Output", command=self.toggle_output_window)
        self.toggle_output_btn.grid(row=2, column=2, padx=5, sticky=EW)

        # Connection Status
        self.status_label = ttk.Label(conn_frame, text="Disconnected", foreground="red")
        self.status_label.grid(row=2, column=3, sticky=W, padx=5)

        # Notebook for different function categories
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # Tabs
        self.gpio_tab = GPIOTab(notebook, self)
        self.pwm_tab = PWMTab(notebook, self)
        self.pulse_tab = PulseTab(notebook, self)
        self.system_tab = SystemTab(notebook, self)
        # ...existing code...
    
    def setup_output_window(self):
        """Setup separate output window"""
        self.output_window = Toplevel(self.root)
        self.output_window.title("Output Log")
        self.output_window.geometry("800x600")
        self.output_window.withdraw()  # Hide by default
        self.output_window.protocol("WM_DELETE_WINDOW", self.hide_output_window)
        
        # Output Frame
        output_frame = ttk.LabelFrame(self.output_window, text="Output", padding=5)
        output_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        self.output = scrolledtext.ScrolledText(output_frame, height=40, state=DISABLED)
        self.output.pack(fill=BOTH, expand=True)
        
        # Clear Output Button
        ttk.Button(output_frame, text="Clear Output", command=self.clear_output).pack(pady=5)
    
    def toggle_output_window(self):
        """Toggle output window visibility"""
        if self.output_window_visible:
            self.hide_output_window()
        else:
            self.show_output_window()
    
    def show_output_window(self):
        """Show output window"""
        self.output_window.deiconify()
        self.output_window.lift()
        self.output_window_visible = True
        self.toggle_output_btn.config(text="Hide Output")
    
    def hide_output_window(self):
        """Hide output window"""
        self.output_window.withdraw()
        self.output_window_visible = False
        self.toggle_output_btn.config(text="Show Output")
    
    
    
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
    
    
    # ...existing code...
    
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
