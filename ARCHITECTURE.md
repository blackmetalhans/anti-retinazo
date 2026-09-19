# 📐 Architectural Specification / Especificación Arquitectónica

> *"There is an idea of an application; some kind of abstraction, but there is no real substance, only an entity, something illusory. And though I can hide my cold gaze, and you can shake my hand and feel flesh gripping yours and maybe you can even sense our lifestyles are probably comparable... I simply am not bloated."*

---

## Language / Idioma
* [🇬🇧 English Documentation](#-english-architecture)
* [🇨🇱 Documentación en Español](#-arquitectura-en-español)

---

# 🇬🇧 English Architecture

### 1. Abstract & System Philosophy
Modern consumer software is a catastrophic monument to incompetence. The average "night mode" utility on GitHub is an Electron monstrosity: three V8 isolates, two IPC bridges, and eighty megabytes of unminified JavaScript merely to adjust three integers on a display adapter. It reeks of mid-level project managers who write LinkedIn posts about "agile velocity" while their software chokes 500 MB of physical RAM.

**Anti-Retinazo** is engineered with clinical misanthropy. It operates directly on the Windows Graphics Device Interface (GDI) hardware Look-Up Table (LUT). 

* **Heap footprint:** < 14 MB (compresses down to < 5 MB upon window minimization).
* **CPU consumption:** 0.000% at rest.
* **Kernel transitions:** Zero polling threads. Pure hardware LUT execution at GPU rasterization scanout.

```
+-------------------------------------------------------------+
|                      USER INTERACTION                       |
|         Tkinter Modern Dark GUI / Slider Event (Tcl/Tk)     |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|               GAMMA ENGINE (gamma_engine.py)                |
|      - Normalizes warmth parameter w in [0.0, 1.0]          |
|      - Computes 3 x 256 monotonic 16-bit Look-Up Tables     |
+-------------------------------------------------------------+
                               |
                               v (ctypes / Win32 C-ABI)
+-------------------------------------------------------------+
|                  USER32 / GDI32 SUBSYSTEM                   |
|   EnumDisplayDevicesW -> CreateDCW(target_display)          |
|   SetDeviceGammaRamp(hdc, &GammaRampStruct)                 |
+-------------------------------------------------------------+
                               |
                               v (Driver DDI / Kernel Mode)
+-------------------------------------------------------------+
|                GPU HARDWARE SCANOUT (DAC / LUT)             |
|   The display controller maps pixel RGB through the RAMDAC  |
|   hardware curve during front-buffer scanout. Zero CPU work.|
+-------------------------------------------------------------+
```

---

### 2. Hardware LUT Scanout & GDI Mechanics

The application does not draw an alpha-blended transparent overlay across the desktop window hierarchy (`WS_EX_TRANSPARENT` / `WS_EX_LAYERED`). Overlays are an insult to engineering: they intercept DWM compositions, degrade desktop frame pacing, interfere with input processing in fullscreen applications, and taint black pixels with muddy brown hues.

Instead, Anti-Retinazo interfaces with `gdi32.dll` via `SetDeviceGammaRamp`. 

```c
typedef struct _RAMP {
    WORD Red[256];
    WORD Green[256];
    WORD Blue[256];
} RAMP, *PRAMP;

BOOL SetDeviceGammaRamp(HDC hDC, LPVOID lpRamp);
BOOL GetDeviceGammaRamp(HDC hDC, LPVOID lpRamp);
```

#### Monotonicity Validation Constraint
The Windows display driver model (WDDM) enforces strict kernel-level validation upon `SetDeviceGammaRamp`:
1. Every vector entry in `Red`, `Green`, and `Blue` must be non-decreasing:
   $$\forall i \in [0, 254], \quad \text{LUT}[i+1] \ge \text{LUT}[i]$$
2. No coefficient may exceed $2^{16}-1 = 65535$.
3. Any violation immediately causes `SetDeviceGammaRamp` to return `FALSE` (`0`), safeguarding against total screen blackouts.

---

### 3. Mathematical Colorimetry & Non-Linear Attenuation

To transition from standard daylight white point ($D_{65} \approx 6500\text{ K}$) down to candle flame ambient warmth ($\approx 2200\text{ K}$), we apply a normalized warmth coefficient $w \in [0.0, 1.0]$.

Given a discrete palette index $i \in [0, 255]$ with base linear quantization:
$$V(i) = \left\lfloor \frac{i}{255.0} \times 65535.0 \right\rfloor$$

The channel transformation vectors are defined as:

$$\begin{aligned}
\text{LUT}_{\text{Red}}(i)   &= \min\left(65535, \max\left(0, \left\lfloor V(i) \times 1.0 \right\rfloor\right)\right) \\
\text{LUT}_{\text{Green}}(i) &= \min\left(65535, \max\left(0, \left\lfloor V(i) \times (1.0 - 0.18 \cdot w) \right\rfloor\right)\right) \\
\text{LUT}_{\text{Blue}}(i)  &= \min\left(65535, \max\left(0, \left\lfloor V(i) \times (1.0 - 0.80 \cdot w) \right\rfloor\right)\right)
\end{aligned}$$

* **Red:** Constant transmission ($100\%$) to preserve baseline photopic luminance.
* **Green:** Mild quadratic dampening (attenuated by up to $18\%$), shifting the chromaticity coordinates away from sickly magenta toward an elegant, radiant amber.
* **Blue:** Aggressive progressive suppression (attenuated by up to $80\%$), eradicating high-energy visible (HEV) radiation in the $400\text{ nm} - 490\text{ nm}$ spectrum.

---

### 4. Multi-Monitor Device Context (HDC) Isolation

Unlike naive implementations that invoke `user32.GetDC(NULL)` and assume a single monolithic framebuffer, Anti-Retinazo enumerates the complete virtual desktop topology:

1. **Topology Query:** Iterates `user32.EnumDisplayDevicesW(NULL, index, &DISPLAY_DEVICEW, 0)`.
2. **Desktop Membership Filter:** Filters strictly for `StateFlags & DISPLAY_DEVICE_ATTACHED_TO_DESKTOP (0x00000001)`.
3. **Explicit Context Creation:** Employs `gdi32.CreateDCW(NULL, DeviceName, NULL, NULL)`.
4. **Lifecycle Segregation:** Explicitly invokes `gdi32.DeleteDC(hdc)` for display-specific contexts, reserving `user32.ReleaseDC(NULL, hdc)` solely for desktop fallback primitives. This eliminates GDI handle leaks with mathematical certainty.

---

### 5. Lifecycle, Signal Interception & Teardown Safety

A gentleman cleans his tools before exiting the room. The program guarantees hardware restoration under three deterministic layers:

1. **Window Close Event (`WM_DELETE_WINDOW`):** Intercepts standard OS termination, writing non-volatile state to `config.json` and firing `restore_original()`.
2. **C-Runtime Exit Handler (`atexit`):** Registers an emergency teardown hook inside the Python runtime to catch standard `sys.exit()` paths.
3. **External Reset Vector (`restaurar_pantalla.bat`):** An atomic one-liner for sudden process termination, resetting all display contexts to neutral linear ramps in under 20 milliseconds.

---
---

# 🇨🇱 Arquitectura en Español

### 1. Resumen y Filosofía del Sistema
El software moderno es un monumento decadente a la pereza intelectual. La típica utilidad de "modo nocturno" en GitHub es un adefesio en Electron: tres instancias de V8, dos puentes IPC y ochenta megabytes de JavaScript sin minificar, todo para mover tres tristes enteros de color en la tarjeta de video. Hiede a scrum masters y mandos medios que publican en LinkedIn sobre "sinergia y agilidad" mientras su software engulle 500 MB de RAM física para dibujar una barra de desplazamiento.

**Anti-Retinazo** fue diseñado con un desprecio clínico hacia el bloatware. Opera directamente sobre la tabla Look-Up Table (LUT) por hardware de la Windows Graphics Device Interface (GDI).

* **Consumo de memoria:** < 14 MB (Windows comprime el Working Set a < 5 MB al minimizar).
* **Consumo de CPU:** 0.000% en reposo.
* **Transiciones de Kernel:** Cero hilos de polling. La curva se aplica a nivel de hardware en el barrido de la tarjeta gráfica (GPU scanout).

---

### 2. Mecánica de Hardware LUT y Windows GDI

Esta herramienta **jamás** crea una ventana transparente (`WS_EX_LAYERED`) encima del escritorio. Las capas transparentes son un insulto a la ingeniería: rompen la composición del Desktop Window Manager (DWM), introducen micro-stuttering en juegos a pantalla completa, secuestran eventos del mouse y tiñen los negros de un marrón mugriento.

Anti-Retinazo interactúa directamente con `gdi32.dll` mediante la función nativa `SetDeviceGammaRamp`.

```c
typedef struct _RAMP {
    WORD Red[256];
    WORD Green[256];
    WORD Blue[256];
} RAMP, *PRAMP;

BOOL SetDeviceGammaRamp(HDC hDC, LPVOID lpRamp);
BOOL GetDeviceGammaRamp(HDC hDC, LPVOID lpRamp);
```

#### Restricción de Monotonía del Driver de Pantalla (WDDM)
El subsistema de video de Windows impone una validación matemática estricta sobre la matriz antes de aplicarla:
1. Cada valor dentro de `Red`, `Green` y `Blue` debe ser monótonamente creciente o igual:
   $$\forall i \in [0, 254], \quad \text{LUT}[i+1] \ge \text{LUT}[i]$$
2. Ningún coeficiente puede exceder $2^{16}-1 = 65535$.
3. Cualquier violación provoca que `SetDeviceGammaRamp` retorne `FALSE` (`0`), evitando de forma nativa que la pantalla se apague en negro.

---

### 3. Colorimetría Matemática y Atenuación No Lineal

Para pasar de la luz de día ($D_{65} \approx 6500\text{ K}$) a la calidez de una vela ($\approx 2200\text{ K}$), normalizamos el factor de calidez $w \in [0.0, 1.0]$.

Dado el índice discreto de paleta $i \in [0, 255]$ y la cuantización lineal base:
$$V(i) = \left\lfloor \frac{i}{255.0} \times 65535.0 \right\rfloor$$

Las funciones de transferencia para cada canal se calculan así:

$$\begin{aligned}
\text{LUT}_{\text{Rojo}}(i)  &= \min\left(65535, \max\left(0, \left\lfloor V(i) \times 1.0 \right\rfloor\right)\right) \\
\text{LUT}_{\text{Verde}}(i) &= \min\left(65535, \max\left(0, \left\lfloor V(i) \times (1.0 - 0.18 \cdot w) \right\rfloor\right)\right) \\
\text{LUT}_{\text{Azul}}(i)  &= \min\left(65535, \max\left(0, \left\lfloor V(i) \times (1.0 - 0.80 \cdot w) \right\rfloor\right)\right)
\end{aligned}$$

* **Rojo:** Transmisión al $100\%$ constante para sostener la luminancia fotópica de lectura.
* **Verde:** Atenuación suave de hasta $18\%$, lo que desvía el tono cromático hacia un ámbar dorado puro, impidiendo tonos violáceos o magentas.
* **Azul:** Supresión progresiva agresiva de hasta el $80\%$, eliminando la radiación electromagnética de alta energía en el rango de $400\text{ nm} - 490\text{ nm}$.

---

### 4. Soporte y Aislamiento Multi-Monitor por Device Context

A diferencia de scripts improvisados que llaman a `user32.GetDC(NULL)` asumiendo un solo monitor, Anti-Retinazo descubre la topología completa del escritorio:

1. **Enumeración:** Ejecuta `user32.EnumDisplayDevicesW(NULL, i, &dd, 0)`.
2. **Filtro de Escritorio:** Selecciona exclusivamente monitores con la bandera `DISPLAY_DEVICE_ATTACHED_TO_DESKTOP`.
3. **Creación de Contexto Directo:** Invoca `gdi32.CreateDCW(NULL, DeviceName, NULL, NULL)` para cada salida física.
4. **Liberación Quirúrgica:** Invoca `gdi32.DeleteDC(hdc)` para contextos dedicados y `user32.ReleaseDC` para el primario, garantizando **cero fugas de GDI handles** en el sistema operativo.

---

### 5. Ciclo de Vida y Seguridad ante Desconexión

Un profesional impecable deja la habitación exactamente como la encontró. El sistema garantiza la restauración de la calibración original mediante tres capas redundantes:

1. **Evento de Cierre (`WM_DELETE_WINDOW`):** Captura el cierre de la ventana, persiste la configuración en `config.json` y ejecuta `restore_original()`.
2. **Hook de C-Runtime (`atexit`):** Atrapa terminaciones normales del intérprete de Python sin depender de la UI.
3. **Vector de Emergencia Independiente (`restaurar_pantalla.bat`):** Un script atómico en batch/python que reinicia todas las curvas a 6500K en menos de 20 milisegundos si alguien mata el proceso por consola.
