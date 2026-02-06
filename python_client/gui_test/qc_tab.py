"""
Tab for QC (Quadrature Counter) functions in ESP32 RPC GUI
"""


from tkinter import *
from tkinter import ttk, messagebox


class QCTab:
    def __init__(self, notebook, parent):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="QC")
        self.parent = parent
        self.setup_qc_tab()

    def _get_channel(self):
        try:
            return int(self.qc_channel_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid channel value")
            return None

    def _extract_value(self, data, preferred_keys=None):
        if isinstance(data, dict):
            if preferred_keys:
                for key in preferred_keys:
                    if key in data:
                        return data[key]
            if len(data) == 1:
                return next(iter(data.values()))
        return data

    def _ensure_connected(self):
        client = self.parent.client
        if not client or not client.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
            return None
        return client

    def execute_qcEnableCounter(self):
        client = self._ensure_connected()
        if not client:
            return
        channel = self._get_channel()
        if channel is None:
            return
        result, msg, _ = client.call_raw("qcEnableCounter", {"channel": channel})
        self.parent.output_message(f"qcEnableCounter({channel}) -> Code: {result}, {msg}")

    def execute_qcDisableCounter(self):
        client = self._ensure_connected()
        if not client:
            return
        channel = self._get_channel()
        if channel is None:
            return
        result, msg, _ = client.call_raw("qcDisableCounter", {"channel": channel})
        self.parent.output_message(f"qcDisableCounter({channel}) -> Code: {result}, {msg}")

    def execute_qcClearCountRegister(self):
        client = self._ensure_connected()
        if not client:
            return
        channel = self._get_channel()
        if channel is None:
            return
        result, msg, _ = client.call_raw("qcClearCountRegister", {"channel": channel})
        self.parent.output_message(f"qcClearCountRegister({channel}) -> Code: {result}, {msg}")
        if result == 0:
            self.qc_count_var.set("0")

    def execute_qcReadCountRegister(self):
        client = self._ensure_connected()
        if not client:
            return
        channel = self._get_channel()
        if channel is None:
            return
        result, msg, data = client.call_raw("qcReadCountRegister", {"channel": channel})
        count = self._extract_value(data, preferred_keys=["count", "value"])
        if result == 0 and count is not None:
            self.qc_count_var.set(str(count))
        else:
            self.qc_count_var.set("-")
        self.parent.output_message(
            f"qcReadCountRegister({channel}) -> Code: {result}, Count: {count}, {msg}"
        )

    def setup_qc_tab(self):
        frame = self.frame

        ttk.Label(frame, text="Quadrature Counter (QC7366)").pack(anchor=W, padx=10, pady=5)

        channel_frame = ttk.Frame(frame)
        channel_frame.pack(fill=X, padx=10, pady=5)
        ttk.Label(channel_frame, text="Channel (0-1):").pack(side=LEFT, padx=5)
        self.qc_channel_var = StringVar(value="0")
        ttk.Combobox(
            channel_frame,
            textvariable=self.qc_channel_var,
            values=("0", "1"),
            width=5,
            state="readonly",
        ).pack(side=LEFT, padx=5)

        ttk.Separator(frame, orient=HORIZONTAL).pack(fill=X, padx=10, pady=10)

        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=X, padx=10, pady=5)
        ttk.Button(control_frame, text="Enable Counter", command=self.execute_qcEnableCounter).pack(
            side=LEFT, padx=5
        )
        ttk.Button(control_frame, text="Disable Counter", command=self.execute_qcDisableCounter).pack(
            side=LEFT, padx=5
        )
        ttk.Button(control_frame, text="Clear Count", command=self.execute_qcClearCountRegister).pack(
            side=LEFT, padx=5
        )

        read_frame = ttk.Frame(frame)
        read_frame.pack(fill=X, padx=10, pady=5)
        ttk.Button(read_frame, text="Read Count", command=self.execute_qcReadCountRegister).pack(
            side=LEFT, padx=5
        )
        ttk.Label(read_frame, text="Count:").pack(side=LEFT, padx=5)
        self.qc_count_var = StringVar(value="-")
        ttk.Label(read_frame, textvariable=self.qc_count_var).pack(side=LEFT, padx=5)
