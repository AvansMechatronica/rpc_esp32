
from tkinter import *
from tkinter import ttk, messagebox

class OLEDRPCTab:
	def __init__(self, notebook, parent):
		self.frame = ttk.Frame(notebook)
		notebook.add(self.frame, text="OLED")
		self.parent = parent
		self.setup_tab()

	def setup_tab(self):
		# OLED Clear Button
		clear_btn = ttk.Button(self.frame, text="Clear OLED", command=self.clear_oled)
		clear_btn.grid(row=0, column=0, padx=10, pady=10, sticky=W)

		# Write Line Section
		ttk.Label(self.frame, text="Line (0-3):").grid(row=1, column=0, sticky=E, padx=5)
		self.line_var = StringVar(value="0")
		line_entry = ttk.Entry(self.frame, textvariable=self.line_var, width=5)
		line_entry.grid(row=1, column=1, sticky=W)

		ttk.Label(self.frame, text="Text:").grid(row=1, column=2, sticky=E, padx=5)
		self.text_var = StringVar()
		text_entry = ttk.Entry(self.frame, textvariable=self.text_var, width=30)
		text_entry.grid(row=1, column=3, sticky=W)

		ttk.Label(self.frame, text="Align:").grid(row=1, column=4, sticky=E, padx=5)
		self.align_var = StringVar(value="0")
		align_combo = ttk.Combobox(self.frame, textvariable=self.align_var, values=["0 (Left)", "1 (Right)", "2 (Center)"], width=10, state="readonly")
		align_combo.grid(row=1, column=5, sticky=W)
		align_combo.current(0)

		write_btn = ttk.Button(self.frame, text="Write Line", command=self.write_line)
		write_btn.grid(row=1, column=6, padx=10, sticky=W)

	def clear_oled(self):
		client = self.parent.client
		if not client or not client.is_connected():
			messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
			return
		result, msg = client._send_command("oledClear")[:2]
		self.parent.output_message(f"oledClear() -> Code: {result}, {msg}")

	def write_line(self):
		client = self.parent.client
		if not client or not client.is_connected():
			messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
			return
		try:
			line = int(self.line_var.get())
			text = self.text_var.get()
			align = int(self.align_var.get()[0])
		except Exception:
			messagebox.showerror("Error", "Invalid input values")
			return
		params = {"line": line, "text": text, "align": align}
		result, msg = client._send_command("oledWriteLine", params)[:2]
		self.parent.output_message(f"oledWriteLine(line={line}, text='{text}', align={align}) -> Code: {result}, {msg}")
