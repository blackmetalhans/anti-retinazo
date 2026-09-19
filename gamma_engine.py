"""
Motor de control de hardware de Gamma Ramp para Windows GDI.
Consumo de CPU: 0.0%
Consumo de RAM: Integrado en el proceso de Python (~12MB).
Modifica directamente la LUT (Look-Up Table) del controlador de video en hardware.
"""

import ctypes
from ctypes import wintypes
import atexit

class GammaRamp(ctypes.Structure):
    _fields_ = [
        ("red", wintypes.WORD * 256),
        ("green", wintypes.WORD * 256),
        ("blue", wintypes.WORD * 256),
    ]

class DISPLAY_DEVICEW(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("DeviceName", wintypes.WCHAR * 32),
        ("DeviceString", wintypes.WCHAR * 128),
        ("StateFlags", wintypes.DWORD),
        ("DeviceID", wintypes.WCHAR * 128),
        ("DeviceKey", wintypes.WCHAR * 128),
    ]

DISPLAY_DEVICE_ATTACHED_TO_DESKTOP = 0x00000001

class GammaEngine:
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.gdi32 = ctypes.windll.gdi32
        self.initial_ramps = {}
        self.backup_original_ramps()
        atexit.register(self.restore_original)

    def get_attached_displays(self):
        """Retorna una lista con los nombres de todos los monitores activos en el escritorio."""
        displays = []
        i = 0
        while True:
            dd = DISPLAY_DEVICEW()
            dd.cb = ctypes.sizeof(DISPLAY_DEVICEW)
            res = self.user32.EnumDisplayDevicesW(None, i, ctypes.byref(dd), 0)
            if not res:
                break
            if dd.StateFlags & DISPLAY_DEVICE_ATTACHED_TO_DESKTOP:
                displays.append(dd.DeviceName)
            i += 1
        return displays if displays else [None]

    def _get_dc_for_display(self, display_name):
        """Obtiene el Device Context (HDC) para un monitor o el escritorio principal."""
        if display_name:
            hdc = self.gdi32.CreateDCW(None, display_name, None, None)
            if hdc:
                return hdc, True
        # Fallback al DC principal
        hdc = self.user32.GetDC(None)
        return hdc, False

    def _release_dc(self, hdc, is_created):
        """Libera correctamente el HDC dependiendo de cómo fue creado."""
        if not hdc:
            return
        if is_created:
            self.gdi32.DeleteDC(hdc)
        else:
            self.user32.ReleaseDC(None, hdc)

    def backup_original_ramps(self):
        """Guarda la calibración original de cada pantalla para restaurar al salir."""
        displays = self.get_attached_displays()
        for disp in displays:
            hdc, is_created = self._get_dc_for_display(disp)
            if hdc:
                ramp = GammaRamp()
                if self.gdi32.GetDeviceGammaRamp(hdc, ctypes.byref(ramp)):
                    self.initial_ramps[disp] = ramp
                self._release_dc(hdc, is_created)

    def calculate_ramp(self, warmth_pct):
        """
        Calcula la curva Gamma para el porcentaje de calidez deseado (0.0 a 100.0).
        - 0%: Pantalla normal (R=1.0, G=1.0, B=1.0)
        - 100%: Filtro de noche profundo (R=1.0, G=0.82, B=0.20)
        Preserva negros profundos y escala suavemente los tonos medios y altos.
        """
        w = max(0.0, min(100.0, float(warmth_pct))) / 100.0

        # Curva de atenuación:
        # El rojo permanece constante para mantener luminosidad.
        # El verde se reduce levemente para virar a ámbar cálido (evitando tonos magenta).
        # El azul se atenúa progresivamente hasta un máximo de ~80% de corte.
        factor_r = 1.0
        factor_g = 1.0 - (0.18 * w)
        factor_b = 1.0 - (0.80 * w)

        ramp = GammaRamp()
        for i in range(256):
            # Escala lineal estándar de 16 bits (0 a 65535)
            val = int((i / 255.0) * 65535.0)
            ramp.red[i] = max(0, min(65535, int(val * factor_r)))
            ramp.green[i] = max(0, min(65535, int(val * factor_g)))
            ramp.blue[i] = max(0, min(65535, int(val * factor_b)))

        return ramp

    def apply_warmth(self, warmth_pct):
        """Aplica la calidez seleccionada a todas las pantallas activas."""
        ramp = self.calculate_ramp(warmth_pct)
        displays = self.get_attached_displays()
        all_success = True

        for disp in displays:
            hdc, is_created = self._get_dc_for_display(disp)
            if hdc:
                res = self.gdi32.SetDeviceGammaRamp(hdc, ctypes.byref(ramp))
                self._release_dc(hdc, is_created)
                if not res:
                    all_success = False
            else:
                all_success = False

        return all_success

    def restore_original(self):
        """Restaura la calibración original de pantalla guardada al inicio."""
        displays = self.get_attached_displays()
        for disp in displays:
            hdc, is_created = self._get_dc_for_display(disp)
            if hdc:
                if disp in self.initial_ramps:
                    self.gdi32.SetDeviceGammaRamp(hdc, ctypes.byref(self.initial_ramps[disp]))
                else:
                    # Si no había respaldo, generar curva lineal limpia (1.0, 1.0, 1.0)
                    neutral_ramp = self.calculate_ramp(0.0)
                    self.gdi32.SetDeviceGammaRamp(hdc, ctypes.byref(neutral_ramp))
                self._release_dc(hdc, is_created)
