
from tkinter import *
from tkinter import ttk, messagebox


class OLEDRPCTab:
	def __init__(self, notebook, parent):
		self.frame = ttk.Frame(notebook)
		notebook.add(self.frame, text="OLED")
		self.parent = parent
		self.setup_tab()

	def setup_tab(self):
		frame = self.frame

		# OLED Clear
		ttk.Label(frame, text="oledClear", font=("Arial", 10, "bold")).pack(anchor=W, padx=10, pady=10)
		clear_frame = ttk.Frame(frame)
		clear_frame.pack(fill=X, padx=10, pady=5)
		clear_btn = ttk.Button(clear_frame, text="Clear OLED", command=self.clear_oled)
		clear_btn.pack(side=LEFT, padx=5)

		ttk.Separator(frame, orient=HORIZONTAL).pack(fill=X, padx=10, pady=10)

		# Write Line
		ttk.Label(frame, text="oledWriteLine", font=("Arial", 10, "bold")).pack(anchor=W, padx=10, pady=10)
		write_frame = ttk.Frame(frame)
		write_frame.pack(fill=X, padx=10, pady=5)

		ttk.Label(write_frame, text="Line (0-3):").pack(side=LEFT, padx=5)
		self.line_var = StringVar(value="0")
		ttk.Combobox(
			write_frame,
			textvariable=self.line_var,
			values=("0", "1", "2", "3"),
			width=5,
			state="readonly",
		).pack(side=LEFT, padx=5)

		ttk.Label(write_frame, text="Text:").pack(side=LEFT, padx=5)
		self.text_var = StringVar()
		ttk.Entry(write_frame, textvariable=self.text_var, width=30).pack(side=LEFT, padx=5)

		ttk.Label(write_frame, text="Align:").pack(side=LEFT, padx=5)
		self.align_var = StringVar(value="0")
		align_combo = ttk.Combobox(
			write_frame,
			textvariable=self.align_var,
			values=["0 (Left)", "1 (Right)", "2 (Center)"],
			width=10,
			state="readonly",
		)
		align_combo.pack(side=LEFT, padx=5)
		align_combo.current(0)

		write_btn = ttk.Button(write_frame, text="Write Line", command=self.write_line)
		write_btn.pack(side=LEFT, padx=5)

	def clear_oled(self):
		client = self.parent.client
		if not client or not client.is_connected():
			messagebox.showwarning("Not Connected", "Please connect to ESP32 first")
			return
		result, msg = client.oledClear()
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
		result, msg = client.oledWriteLine(line, text, align)
		self.parent.output_message(f"oledWriteLine(line={line}, text='{text}', align={align}) -> Code: {result}, {msg}")
