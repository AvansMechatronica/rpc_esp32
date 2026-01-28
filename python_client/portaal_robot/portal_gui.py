#!/usr/bin/env python3
"""
Portal robot GUI to drive three stepper axes (X, Y, Z) over USB or WiFi.
- Reads configurable pin/channel/speed settings from YAML or JSON
- Supports absolute and relative moves with fields and sliders
- Shows per-axis progress and independent stop buttons
- Provides an emergency stop that halts all axes
- Displays the portaalrobot.jpg reference image in the UI
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import json
import logging
import pathlib
import sys
import tkinter as tk
from dataclasses import dataclass, field
from tkinter import filedialog, messagebox, scrolledtext, ttk
from typing import Dict, Optional

from PIL import Image, ImageTk

from library.config import COMM_USB, COMM_WIFI, CONFIG, RPC_OK, setup_logging
from library.rpc_client import RPCClient

try:
    import yaml
except ImportError:  # pragma: no cover - PyYAML is listed in requirements
    yaml = None

logger = logging.getLogger(__name__)


@dataclass
class MotorConfig:
    axis: str
    channel: int
    step_pin: int
    dir_pin: int
    pulses_per_unit: float
    unit_name: str
    soft_min: float
    soft_max: float
    start_position: float
    pulse_width_ms: int
    pause_width_ms: int


@dataclass
class MotorState:
    cfg: MotorConfig
    position: float = 0.0
    pending_delta: float = 0.0
    total_pulses: int = 0
    remaining_pulses: int = 0
    moving: bool = False
    mode_var: tk.StringVar = field(default_factory=lambda: tk.StringVar(value="abs"))
    abs_var: tk.DoubleVar = field(default_factory=lambda: tk.DoubleVar(value=0.0))
    rel_var: tk.DoubleVar = field(default_factory=lambda: tk.DoubleVar(value=0.0))
    progress_var: tk.DoubleVar = field(default_factory=lambda: tk.DoubleVar(value=0.0))
    status_var: tk.StringVar = field(default_factory=lambda: tk.StringVar(value="Idle"))


class PortalRobotGUI:
    def __init__(self, root: tk.Tk, config_path: pathlib.Path):
        self.root = root
        self.root.title("Portal Robot Controller")
        self.root.geometry("1280x820")
        self.config_path = config_path
        self.config_data = self._load_config(config_path)
        self.client: Optional[RPCClient] = None
        self.connected = False
        self.motors: Dict[str, MotorState] = {}
        self.poll_interval_ms = int(self.config_data.get("motion", {}).get("poll_interval_ms", 120))
        self.output_window: Optional[tk.Toplevel] = None
        self.output_text: Optional[scrolledtext.ScrolledText] = None
        self.output_visible = False

        self._build_style()
        self._build_layout()
        self._build_output_window()
        self._init_motors()
        self._update_connection_status()

    def _load_config(self, path: pathlib.Path) -> dict:
        if not path.exists():
            self._popup_error("Config ontbreekt", f"Configuratiebestand niet gevonden: {path}")
            sys.exit(1)
        with path.open("r", encoding="utf-8") as f:
            text = f.read()
        suffix = path.suffix.lower()
        try:
            if suffix in (".yaml", ".yml"):
                if yaml is None:
                    raise RuntimeError("PyYAML ontbreekt; installeer eerst de dependencies")
                return yaml.safe_load(text) or {}
            return json.loads(text)
        except Exception as exc:  # pragma: no cover - interactive path
            self._popup_error("Config fout", f"Kon configuratie niet laden: {exc}")
            sys.exit(1)

    def _build_style(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        base_font = ("Helvetica", 11)
        style.configure("TLabel", font=base_font)
        style.configure("TButton", font=base_font)
        style.configure("Title.TLabel", font=("Helvetica", 14, "bold"))
        style.configure("Axis.TLabelframe", font=("Helvetica", 12, "bold"))
        style.configure("Axis.TLabelframe.Label", font=("Helvetica", 12, "bold"))
        style.configure("Danger.TButton", font=("Helvetica", 12, "bold"), foreground="white", background="#b3261e")

    def _build_layout(self) -> None:
        top = ttk.Frame(self.root, padding=12)
        top.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(top)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right = ttk.Frame(top, width=420)
        right.pack(side=tk.RIGHT, fill=tk.BOTH)
        right.pack_propagate(False)

        self._build_connection_panel(left)
        self._build_motors_panel(left)
        self._build_emergency_panel(left)
        self._build_image_panel(right)

    def _build_connection_panel(self, parent: ttk.Frame) -> None:
        frame = ttk.LabelFrame(parent, text="Verbinding", padding=10)
        frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frame, text="Modus:").grid(row=0, column=0, sticky=tk.W, padx=4, pady=2)
        self.mode_var = tk.StringVar(value=self.config_data.get("transport", {}).get("mode", "usb").lower())
        mode_combo = ttk.Combobox(frame, textvariable=self.mode_var, values=["usb", "wifi"], state="readonly", width=10)
        mode_combo.grid(row=0, column=1, padx=4, pady=2)

        ttk.Label(frame, text="USB poort:").grid(row=0, column=2, sticky=tk.W, padx=4, pady=2)
        self.usb_port_var = tk.StringVar(value=str(self.config_data.get("transport", {}).get("usb_port", "/dev/ttyUSB0")))
        ttk.Entry(frame, textvariable=self.usb_port_var, width=16).grid(row=0, column=3, padx=4, pady=2)

        ttk.Label(frame, text="WiFi host:").grid(row=1, column=0, sticky=tk.W, padx=4, pady=2)
        self.wifi_host_var = tk.StringVar(value=str(self.config_data.get("transport", {}).get("wifi_host", "192.168.1.100")))
        ttk.Entry(frame, textvariable=self.wifi_host_var, width=16).grid(row=1, column=1, padx=4, pady=2)

        ttk.Label(frame, text="WiFi poort:").grid(row=1, column=2, sticky=tk.W, padx=4, pady=2)
        self.wifi_port_var = tk.StringVar(value=str(self.config_data.get("transport", {}).get("wifi_port", 5000)))
        ttk.Entry(frame, textvariable=self.wifi_port_var, width=10).grid(row=1, column=3, padx=4, pady=2)

        ttk.Button(frame, text="Verbind", command=self.connect).grid(row=2, column=0, pady=8, sticky=tk.EW)
        ttk.Button(frame, text="Verbreek", command=self.disconnect).grid(row=2, column=1, pady=8, sticky=tk.EW)
        ttk.Button(frame, text="Laad config", command=self._choose_config).grid(row=2, column=2, pady=8, sticky=tk.EW)
        self.toggle_log_btn = ttk.Button(frame, text="Toon log", command=self.toggle_output_window)
        self.toggle_log_btn.grid(row=2, column=3, pady=8, sticky=tk.EW)

        self.connection_label = ttk.Label(frame, text="Niet verbonden", foreground="red")
        self.connection_label.grid(row=3, column=0, columnspan=4, sticky=tk.W, pady=(4, 0))

    def _build_motors_panel(self, parent: ttk.Frame) -> None:
        # Create a frame to hold the canvas and scrollbar
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Create a canvas and a vertical scrollbar for it
        canvas = tk.Canvas(container, borderwidth=0, highlightthickness=0)
        vscroll = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vscroll.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vscroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Create the actual motors frame inside the canvas
        self.motors_frame = ttk.LabelFrame(canvas, text="Motoren", padding=10)
        motors_frame_id = canvas.create_window((0, 0), window=self.motors_frame, anchor="nw")

        # Update scrollregion when the size of the frame changes
        def _on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.motors_frame.bind("<Configure>", _on_frame_configure)

        # Make sure the frame width tracks the canvas width
        def _on_canvas_configure(event):
            canvas.itemconfig(motors_frame_id, width=event.width)
        canvas.bind("<Configure>", _on_canvas_configure)

    def _build_emergency_panel(self, parent: ttk.Frame) -> None:
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X)
        ttk.Button(frame, text="NOODSTOP", command=self.emergency_stop, style="Danger.TButton").pack(fill=tk.X)

    def _build_image_panel(self, parent: ttk.Frame) -> None:
        img_path = pathlib.Path(__file__).with_name("portaalrobot.jpg")
        self.photo_label = ttk.Label(parent, text="portaalrobot.jpg niet gevonden", anchor="center")
        self.photo_label.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        if img_path.exists():
            try:
                image = Image.open(img_path)
                image = image.resize((400, 400), Image.LANCZOS)
                self.photo = ImageTk.PhotoImage(image)
                self.photo_label.configure(image=self.photo, text="")
            except Exception as exc:  # pragma: no cover - visual path
                self.photo_label.configure(text=f"Afbeelding laden mislukt: {exc}")

    def _build_output_window(self) -> None:
        self.output_window = tk.Toplevel(self.root)
        self.output_window.title("Log")
        self.output_window.geometry("700x400")
        self.output_window.withdraw()
        self.output_window.protocol("WM_DELETE_WINDOW", self.hide_output_window)

        frame = ttk.Frame(self.output_window, padding=8)
        frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(frame, height=18, state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        clear_btn = ttk.Button(frame, text="Wis log", command=self.clear_output)
        clear_btn.pack(anchor=tk.E, pady=6)

    def _init_motors(self) -> None:
        motion_cfg = self.config_data.get("motion", {})
        default_pulse_width = int(motion_cfg.get("pulse_width_ms", 2))
        default_pause_width = int(motion_cfg.get("pause_width_ms", 2))
        motors_cfg = self.config_data.get("motors", {})

        for child in list(self.motors_frame.winfo_children()):
            child.destroy()

        row = 0
        for axis_key in ("x", "y", "z"):
            cfg_raw = motors_cfg.get(axis_key)
            if not cfg_raw:
                continue
            cfg = MotorConfig(
                axis=axis_key.upper(),
                channel=int(cfg_raw.get("channel")),
                step_pin=int(cfg_raw.get("step_pin")),
                dir_pin=int(cfg_raw.get("dir_pin")),
                pulses_per_unit=float(cfg_raw.get("pulses_per_unit", 200)),
                unit_name=str(cfg_raw.get("unit_name", "mm")),
                soft_min=float(cfg_raw.get("soft_min", 0)),
                soft_max=float(cfg_raw.get("soft_max", 0)),
                start_position=float(cfg_raw.get("start_position", 0)),
                pulse_width_ms=int(cfg_raw.get("pulse_width_ms", default_pulse_width)),
                pause_width_ms=int(cfg_raw.get("pause_width_ms", default_pause_width)),
            )
            state = MotorState(cfg=cfg, position=cfg.start_position)
            state.abs_var.set(cfg.start_position)
            self.motors[axis_key] = state
            frame = ttk.LabelFrame(self.motors_frame, text=f"As {cfg.axis}", padding=10, style="Axis.TLabelframe")
            frame.grid(row=row, column=0, sticky="nsew", pady=6)
            self._build_motor_controls(frame, axis_key, state)
            row += 1

        self.motors_frame.columnconfigure(0, weight=1)

    def _build_motor_controls(self, frame: ttk.Labelframe, axis_key: str, state: MotorState) -> None:
        cfg = state.cfg

        header = ttk.Frame(frame)
        header.pack(fill=tk.X, pady=(0, 6))
        state.position_label = ttk.Label(header, text=self._position_text(state))
        state.position_label.pack(side=tk.LEFT, padx=8)

        mode_frame = ttk.Frame(frame)
        mode_frame.pack(fill=tk.X, pady=4)
        ttk.Radiobutton(mode_frame, text="Absoluut", variable=state.mode_var, value="abs").pack(side=tk.LEFT, padx=4)
        ttk.Radiobutton(mode_frame, text="Relatief", variable=state.mode_var, value="rel").pack(side=tk.LEFT, padx=4)

        abs_frame = ttk.Frame(frame)
        abs_frame.pack(fill=tk.X, pady=4)
        ttk.Label(abs_frame, text=f"Doel ({cfg.unit_name}):").pack(side=tk.LEFT)
        abs_entry = ttk.Entry(abs_frame, textvariable=state.abs_var, width=10)
        abs_entry.pack(side=tk.LEFT, padx=4)
        abs_entry.bind("<FocusOut>", lambda _e, s=state: self._sync_abs_slider(s))

        slider = ttk.Scale(frame, from_=cfg.soft_min, to=cfg.soft_max, orient=tk.HORIZONTAL, variable=state.abs_var,
                           command=lambda _v, s=state: self._on_slider_change(s))
        slider.pack(fill=tk.X, pady=2)
        state.slider = slider

        rel_frame = ttk.Frame(frame)
        rel_frame.pack(fill=tk.X, pady=4)
        ttk.Label(rel_frame, text=f"Relatief ({cfg.unit_name}):").pack(side=tk.LEFT)
        ttk.Entry(rel_frame, textvariable=state.rel_var, width=10).pack(side=tk.LEFT, padx=4)

        action_frame = ttk.Frame(frame)
        action_frame.pack(fill=tk.X, pady=6)
        ttk.Button(action_frame, text="Start", command=lambda a=axis_key: self.start_move(a)).pack(side=tk.LEFT, padx=4)
        ttk.Button(action_frame, text="Stop", command=lambda a=axis_key: self.stop_motor(a)).pack(side=tk.LEFT, padx=4)

        progress_frame = ttk.Frame(frame)
        progress_frame.pack(fill=tk.X)
        ttk.Label(progress_frame, textvariable=state.status_var).pack(side=tk.LEFT)
        progress = ttk.Progressbar(progress_frame, variable=state.progress_var, maximum=100)
        progress.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=4)
        state.progress = progress

    def _position_text(self, state: MotorState) -> str:
        return f"Huidig: {state.position:.3f} {state.cfg.unit_name}"

    def _popup_info(self, title: str, message: str) -> None:
        self._log(f"[INFO] {title}: {message}")
        messagebox.showinfo(title, message)

    def _popup_warning(self, title: str, message: str) -> None:
        self._log(f"[WARN] {title}: {message}")
        messagebox.showwarning(title, message)

    def _popup_error(self, title: str, message: str) -> None:
        self._log(f"[ERROR] {title}: {message}")
        messagebox.showerror(title, message)

    def toggle_output_window(self) -> None:
        if self.output_visible:
            self.hide_output_window()
        else:
            self.show_output_window()

    def show_output_window(self) -> None:
        if not self.output_window:
            return
        self.output_window.deiconify()
        self.output_window.lift()
        self.output_visible = True
        if self.toggle_log_btn:
            self.toggle_log_btn.configure(text="Verberg log")

    def hide_output_window(self) -> None:
        if not self.output_window:
            return
        self.output_window.withdraw()
        self.output_visible = False
        if self.toggle_log_btn:
            self.toggle_log_btn.configure(text="Toon log")

    def clear_output(self) -> None:
        if not self.output_text:
            return
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)

    def _log(self, message: str) -> None:
        logger.info(message)
        if not self.output_text:
            return
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)

    def _on_slider_change(self, state: MotorState) -> None:
        state.abs_var.set(round(state.abs_var.get(), 3))

    def _sync_abs_slider(self, state: MotorState) -> None:
        try:
            value = float(state.abs_var.get())
        except ValueError:
            value = state.position
        value = max(state.cfg.soft_min, min(state.cfg.soft_max, value))
        state.abs_var.set(value)

    def _choose_config(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Kies configuratie",
            filetypes=[("YAML", "*.yaml *.yml"), ("JSON", "*.json"), ("Alle bestanden", "*.*")],
            initialdir=str(self.config_path.parent),
        )
        if not file_path:
            return
        self.config_path = pathlib.Path(file_path)
        self.config_data = self._load_config(self.config_path)
        self._init_motors()
        self._popup_info("Config geladen", f"Nieuwe configuratie geladen uit {self.config_path.name}")

    def connect(self) -> None:
        if self.connected:
            return
        mode_text = self.mode_var.get().lower()
        mode = COMM_USB if mode_text == "usb" else COMM_WIFI
        kwargs = {}
        if mode == COMM_USB:
            kwargs["port"] = self.usb_port_var.get()
            kwargs["baudrate"] = int(self.config_data.get("transport", {}).get("usb_baudrate", CONFIG.get("usb_baudrate", 115200)))
        else:
            kwargs["host"] = self.wifi_host_var.get()
            kwargs["port"] = int(self.wifi_port_var.get())

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        self.client = RPCClient(comm_mode=mode, **kwargs)
        success, msg = self.client.connect()
        if not success:
            self._popup_error("Verbinding mislukt", msg)
            self._log(f"Verbinding mislukt: {msg}")
            return

        if not self._initialize_hardware():
            return

        self.connected = True
        self._update_connection_status()
        self._log("Verbonden met ESP32")
        self._popup_info("Verbonden", "Verbonden met ESP32")

    def _initialize_hardware(self) -> bool:
        assert self.client is not None
        for axis_key, state in self.motors.items():
            cfg = state.cfg
            res, msg = self.client.pinMode(cfg.dir_pin, 1)
            if res != RPC_OK:
                self._popup_error("Init fout", f"As {cfg.axis}: pinMode dir mislukt: {msg}")
                return False
            res, msg = self.client.pulseBegin(cfg.channel, cfg.step_pin)
            if res != RPC_OK:
                self._popup_error("Init fout", f"As {cfg.axis}: pulseBegin mislukt: {msg}")
                return False
        return True

    def disconnect(self) -> None:
        if self.client:
            try:
                self.client.disconnect()
            except Exception:
                logger.exception("Disconnect failed")
                self._log("Fout bij verbreken van verbinding")
        self.connected = False
        self._update_connection_status()
        self._log("Verbinding verbroken")

    def _update_connection_status(self) -> None:
        if self.connected:
            self.connection_label.configure(text="Verbonden", foreground="green")
        else:
            self.connection_label.configure(text="Niet verbonden", foreground="red")

    def _ensure_client(self) -> bool:
        if not self.client or not self.client.is_connected():
            self._popup_warning("Niet verbonden", "Maak eerst verbinding met de ESP32")
            return False
        return True

    def start_move(self, axis_key: str) -> None:
        if not self._ensure_client():
            return
        state = self.motors[axis_key]
        cfg = state.cfg
        try:
            if state.mode_var.get() == "abs":
                delta = float(state.abs_var.get()) - state.position
            else:
                delta = float(state.rel_var.get())
        except ValueError:
            self._popup_error("Ongeldige invoer", "Gebruik numerieke waarden voor bewegingen")
            return

        if abs(delta) < 1e-6:
            self._popup_info("Geen beweging", "Doelwaarde is gelijk aan huidige positie")
            return

        pulses = int(round(abs(delta) * cfg.pulses_per_unit))
        if pulses <= 0:
            self._popup_error("Beweging te klein", "Aantal pulses komt uit op nul")
            return

        direction = 1 if delta > 0 else 0

        res, msg = self.client.digitalWrite(cfg.dir_pin, direction)
        if res != RPC_OK:
            self._popup_error("Richting fout", msg)
            self._log(f"As {cfg.axis}: richting zetten mislukt: {msg}")
            return

        state.pending_delta = delta
        state.total_pulses = pulses
        state.remaining_pulses = pulses
        state.moving = True
        state.status_var.set("Bezig...")
        state.progress_var.set(0)
        self._log(f"As {cfg.axis}: start {'abs' if state.mode_var.get()=='abs' else 'rel'} move, delta={delta:.3f} {cfg.unit_name}, pulses={pulses}")

        res, msg = self.client.generatePulsesAsync(
            cfg.channel,
            cfg.pulse_width_ms,
            cfg.pause_width_ms,
            pulses,
        )
        if res != RPC_OK:
            state.moving = False
            state.status_var.set("Idle")
            self._popup_error("Start mislukt", msg)
            self._log(f"As {cfg.axis}: start mislukt: {msg}")
            return

        self._schedule_poll(axis_key)

    def _schedule_poll(self, axis_key: str) -> None:
        self.root.after(self.poll_interval_ms, lambda a=axis_key: self._poll_motor(a))

    def _poll_motor(self, axis_key: str) -> None:
        if not self.connected:
            return
        state = self.motors[axis_key]
        cfg = state.cfg
        if not state.moving:
            return

        res, msg, remaining = self.client.getRemainingPulses(cfg.channel)
        if res == RPC_OK and remaining is not None:
            state.remaining_pulses = remaining
            done = max(0, min(1.0, 1 - (remaining / max(1, state.total_pulses))))
            state.progress_var.set(done * 100)
        else:
            logger.warning("getRemainingPulses mislukt voor %s: %s", cfg.axis, msg)

        res, msg, pulsing = self.client.isPulsing(cfg.channel)
        if res != RPC_OK:
            logger.warning("isPulsing mislukt voor %s: %s", cfg.axis, msg)
            self._log(f"As {cfg.axis}: status check mislukt: {msg}")
            self._schedule_poll(axis_key)
            return

        if pulsing:
            self._schedule_poll(axis_key)
            return

        state.moving = False
        state.position += state.pending_delta
        state.status_var.set("Klaar")
        state.progress_var.set(100)
        state.abs_var.set(state.position)
        state.rel_var.set(0)
        state.position_label.configure(text=self._position_text(state))
        self._log(f"As {cfg.axis}: gereed, nieuwe positie {state.position:.3f} {cfg.unit_name}")

    def stop_motor(self, axis_key: str) -> None:
        if not self._ensure_client():
            return
        state = self.motors[axis_key]
        cfg = state.cfg
        res, msg = self.client.stopPulse(cfg.channel)
        if res != RPC_OK:
            self._popup_error("Stop mislukt", msg)
            self._log(f"As {cfg.axis}: stop mislukt: {msg}")
            return
        # Update position to current hardware value if possible
        try:
            res, msg, value = self.client.getPosition(cfg.channel)
            if res == RPC_OK and value is not None:
                state.position = value
        except Exception:
            pass
        state.moving = False
        state.status_var.set("Gestopt")
        state.progress_var.set(0)
        state.pending_delta = 0
        state.remaining_pulses = 0
        state.abs_var.set(state.position)
        state.rel_var.set(0)
        state.position_label.configure(text=self._position_text(state))
        self._log(f"As {cfg.axis}: gestopt, positie onthouden: {state.position:.3f} {cfg.unit_name}")

    def emergency_stop(self) -> None:
        if not self._ensure_client():
            return
        for axis_key, state in self.motors.items():
            cfg = state.cfg
            res, msg = self.client.stopPulse(cfg.channel)
            if res != RPC_OK:
                logger.warning("Noodstop fout op %s: %s", cfg.axis, msg)
                self._log(f"As {cfg.axis}: noodstop fout: {msg}")
            # Update position to current hardware value if possible
            try:
                res2, msg2, value = self.client.getPosition(cfg.channel)
                if res2 == RPC_OK and value is not None:
                    state.position = value
            except Exception:
                pass
            state.moving = False
            state.status_var.set("NOODSTOP")
            state.progress_var.set(0)
            state.pending_delta = 0
            state.remaining_pulses = 0
            state.abs_var.set(state.position)
            state.rel_var.set(0)
            state.position_label.configure(text=self._position_text(state))
        self._log("Noodstop: alle motoren gestopt en posities onthouden")
        self._popup_warning("Noodstop", "Alle motoren zijn gestopt")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Portal robot GUI")
    parser.add_argument("--config", default="portal_config.yaml", help="Pad naar YAML/JSON configuratie")
    parser.add_argument("--debug", type=int, default=0, choices=[0, 1, 2, 3, 4], help="Debug niveau (0-4)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    setup_logging(debug_level=args.debug)
    # Always try to load portal_config.yaml from script dir if no --config given or file not found
    config_path = pathlib.Path(args.config)
    if not config_path.exists():
        # Try script dir
        script_dir = pathlib.Path(__file__).parent
        fallback = script_dir / "portal_config.yaml"
        if fallback.exists():
            config_path = fallback
    root = tk.Tk()
    app = PortalRobotGUI(root, config_path)
    root.mainloop()


if __name__ == "__main__":
    main()
