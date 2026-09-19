#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filtro de Luz Azul Ultra-Ligero para Windows
Arquitectura: Windows GDI Hardware Gamma Ramp
Consumo: ~12-14 MB RAM | 0.0% CPU
Zero-Dependencies (Solo librerías estándar de Python)
"""

import sys
import os
import json
import tkinter as tk
from tkinter import ttk
import ctypes

# Asegurar renderizado nítido en pantallas de alta resolución (DPI scaling)
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

# Importar motor Gamma
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from gamma_engine import GammaEngine

CONFIG_FILE = os.path.join(script_dir, "config.json")

def load_config():
    default_cfg = {
        "active": False,
        "warmth": 60,
        "restore_on_close": True
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return {**default_cfg, **json.load(f)}
        except Exception:
            pass
    return default_cfg

def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except Exception:
        pass

class BlueLightFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Filtro de Luz Azul")
        self.root.geometry("380x560")
        self.root.resizable(False, False)
        self.root.configure(bg="#121214")

        # Centrar ventana en pantalla
        self.center_window()

        self.engine = GammaEngine()
        self.config = load_config()

        self.is_active = self.config.get("active", False)
        self.warmth_val = self.config.get("warmth", 60)
        self.restore_on_close_var = tk.BooleanVar(value=self.config.get("restore_on_close", True))

        # Colores de interfaz
        self.c_bg = "#121214"
        self.c_card = "#1a1a1e"
        self.c_card_border = "#2b2b32"
        self.c_text_title = "#f4f4f5"
        self.c_text_muted = "#a1a1aa"
        self.c_amber = "#f59e0b"
        self.c_emerald = "#10b981"
        self.c_gray_btn = "#27272a"
        self.c_gray_btn_hover = "#3f3f46"

        self.build_ui()

        # Si estaba activo al guardar, aplicar filtro
        if self.is_active:
            self.engine.apply_warmth(self.warmth_val)
            self.update_active_ui(True)
        else:
            self.update_active_ui(False)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def center_window(self):
        self.root.update_idletasks()
        w = 380
        h = 560
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = int((ws / 2) - (w / 2))
        y = int((hs / 2) - (h / 2))
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def build_ui(self):
        # Contenedor principal con padding
        main_frame = tk.Frame(self.root, bg=self.c_bg, padx=22, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = tk.Frame(main_frame, bg=self.c_bg)
        header_frame.pack(fill=tk.X, pady=(0, 16))

        title_lbl = tk.Label(
            header_frame,
            text="🌙 Filtro de Luz Azul",
            font=("Segoe UI", 16, "bold"),
            fg=self.c_text_title,
            bg=self.c_bg
        )
        title_lbl.pack(anchor="w")

        sub_lbl = tk.Label(
            header_frame,
            text="Win32 Hardware GDI · 0% CPU · ~12MB RAM",
            font=("Segoe UI", 9),
            fg="#71717a",
            bg=self.c_bg
        )
        sub_lbl.pack(anchor="w", pady=(2, 0))

        # Tarjeta de Switch Principal (ON / OFF)
        self.card_toggle = tk.Frame(
            main_frame,
            bg=self.c_card,
            highlightbackground=self.c_card_border,
            highlightthickness=1,
            padx=16,
            pady=16
        )
        self.card_toggle.pack(fill=tk.X, pady=(0, 18))

        self.status_lbl = tk.Label(
            self.card_toggle,
            text="ESTADO: DESACTIVADO",
            font=("Segoe UI", 10, "bold"),
            fg="#71717a",
            bg=self.c_card
        )
        self.status_lbl.pack(anchor="center", pady=(0, 10))

        self.btn_toggle = tk.Button(
            self.card_toggle,
            text="⏻ ACTIVAR FILTRO",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#27272a",
            activebackground="#3f3f46",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=10,
            command=self.toggle_filter
        )
        self.btn_toggle.pack(fill=tk.X)

        # Tarjeta de Calidez / Slider
        card_slider = tk.Frame(
            main_frame,
            bg=self.c_card,
            highlightbackground=self.c_card_border,
            highlightthickness=1,
            padx=16,
            pady=16
        )
        card_slider.pack(fill=tk.X, pady=(0, 16))

        slider_header = tk.Frame(card_slider, bg=self.c_card)
        slider_header.pack(fill=tk.X, pady=(0, 4))

        slider_title = tk.Label(
            slider_header,
            text="Intensidad de Calidez",
            font=("Segoe UI", 10, "bold"),
            fg=self.c_text_title,
            bg=self.c_card
        )
        slider_title.pack(side=tk.LEFT)

        self.val_lbl = tk.Label(
            slider_header,
            text=f"{int(self.warmth_val)}%",
            font=("Segoe UI", 13, "bold"),
            fg=self.c_amber,
            bg=self.c_card
        )
        self.val_lbl.pack(side=tk.RIGHT)

        # Estimación de temperatura (Kelvin)
        self.temp_lbl = tk.Label(
            card_slider,
            text=self.get_temp_str(self.warmth_val),
            font=("Segoe UI", 9),
            fg=self.c_text_muted,
            bg=self.c_card
        )
        self.temp_lbl.pack(anchor="w", pady=(0, 10))

        # Slider Tkinter con estilo oscuro
        self.scale = tk.Scale(
            card_slider,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            showvalue=0,
            resolution=1,
            bg=self.c_card,
            troughcolor="#2e2e38",
            activebackground=self.c_amber,
            highlightthickness=0,
            bd=0,
            sliderrelief=tk.FLAT,
            command=self.on_slider_change,
            cursor="hand2"
        )
        self.scale.set(self.warmth_val)
        self.scale.pack(fill=tk.X, pady=(0, 12))

        # Presets rápidos
        presets_lbl = tk.Label(
            card_slider,
            text="PRESETS RÁPIDOS",
            font=("Segoe UI", 8, "bold"),
            fg="#71717a",
            bg=self.c_card
        )
        presets_lbl.pack(anchor="w", pady=(4, 6))

        presets_row = tk.Frame(card_slider, bg=self.c_card)
        presets_row.pack(fill=tk.X)

        presets = [
            ("Día (0%)", 0),
            ("Tarde (35%)", 35),
            ("Noche (65%)", 65),
            ("Velas (85%)", 85)
        ]

        for text, val in presets:
            btn = tk.Button(
                presets_row,
                text=text,
                font=("Segoe UI", 8),
                fg=self.c_text_title,
                bg="#27272a",
                activebackground=self.c_amber,
                activeforeground="#000000",
                relief=tk.FLAT,
                cursor="hand2",
                padx=5,
                pady=4,
                command=lambda v=val: self.apply_preset(v)
            )
            btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        # Opciones
        opts_frame = tk.Frame(main_frame, bg=self.c_bg)
        opts_frame.pack(fill=tk.X, pady=(4, 0))

        chk_restore = tk.Checkbutton(
            opts_frame,
            text="Restaurar pantalla al cerrar ventana",
            variable=self.restore_on_close_var,
            font=("Segoe UI", 9),
            fg=self.c_text_muted,
            bg=self.c_bg,
            selectcolor=self.c_card,
            activebackground=self.c_bg,
            activeforeground=self.c_text_title
        )
        chk_restore.pack(anchor="w")

        # Consejo de minimización
        tip_lbl = tk.Label(
            main_frame,
            text="💡 Tip: Minimiza (_) para mantenerlo activo en\nsegundo plano sin gastar memoria ni CPU.",
            font=("Segoe UI", 8),
            fg="#71717a",
            bg=self.c_bg,
            justify=tk.LEFT
        )
        tip_lbl.pack(anchor="w", pady=(10, 0))

    def get_temp_str(self, warmth):
        w = float(warmth)
        if w <= 0:
            return "6500 K · Luz neutra de día (Sin filtro)"
        elif w <= 30:
            return f"~{int(6500 - w*40)} K · Filtro leve (Cansancio ocular)"
        elif w <= 60:
            return f"~{int(5300 - (w-30)*40)} K · Modo noche confortable"
        elif w <= 85:
            return f"~{int(4100 - (w-60)*50)} K · Descanso pre-sueño"
        else:
            return f"~{int(2850 - (w-85)*50)} K · Ultra cálido (Velas / Tono ámbar)"

    def on_slider_change(self, val):
        self.warmth_val = float(val)
        self.val_lbl.config(text=f"{int(self.warmth_val)}%")
        self.temp_lbl.config(text=self.get_temp_str(self.warmth_val))

        # Si el filtro está encendido, actualizar inmediatamente en hardware
        if self.is_active:
            self.engine.apply_warmth(self.warmth_val)
        elif self.warmth_val > 0:
            # Si el usuario mueve el slider, activar automáticamente para previsualizar
            self.is_active = True
            self.engine.apply_warmth(self.warmth_val)
            self.update_active_ui(True)

    def apply_preset(self, val):
        self.scale.set(val)
        self.warmth_val = val
        self.val_lbl.config(text=f"{int(val)}%")
        self.temp_lbl.config(text=self.get_temp_str(val))

        if val == 0:
            self.is_active = False
            self.engine.restore_original()
            self.update_active_ui(False)
        else:
            self.is_active = True
            self.engine.apply_warmth(self.warmth_val)
            self.update_active_ui(True)

    def toggle_filter(self):
        if self.is_active:
            self.is_active = False
            self.engine.restore_original()
            self.update_active_ui(False)
        else:
            self.is_active = True
            if self.warmth_val == 0:
                self.warmth_val = 60
                self.scale.set(60)
            self.engine.apply_warmth(self.warmth_val)
            self.update_active_ui(True)

    def update_active_ui(self, active):
        if active:
            self.status_lbl.config(text="ESTADO: ACTIVADO (CÁLIDO)", fg=self.c_emerald)
            self.btn_toggle.config(
                text="✓ FILTRO ACTIVO (Clic para apagar)",
                bg=self.c_emerald,
                activebackground="#059669"
            )
            self.card_toggle.config(highlightbackground=self.c_emerald)
        else:
            self.status_lbl.config(text="ESTADO: DESACTIVADO (NORMAL)", fg="#71717a")
            self.btn_toggle.config(
                text="⏻ ACTIVAR FILTRO",
                bg="#27272a",
                activebackground="#3f3f46"
            )
            self.card_toggle.config(highlightbackground=self.c_card_border)

    def on_close(self):
        save_config({
            "active": self.is_active,
            "warmth": self.warmth_val,
            "restore_on_close": self.restore_on_close_var.get()
        })
        if self.restore_on_close_var.get():
            self.engine.restore_original()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BlueLightFilterApp(root)
    root.mainloop()
