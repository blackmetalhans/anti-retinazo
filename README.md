# 🩸 Anti-Retinazo

> *"Look at that subtle 12-megabyte resident set size. The tasteful monotonicity of the hardware look-up table. Oh, my God. It doesn't even spawn a node_modules folder."*

---

## Language / Idioma
* [🇬🇧 English Version](#-english-overview)
* [🇨🇱 Versión en Español](#-descripción-en-español)
* [📐 Deep Architecture / Especificación Arquitectónica](ARCHITECTURE.md)

---

# 🇬🇧 English Overview

### The Problem with Mediocrity

In the evening, before I sit down to review my quarterly portfolios, I observe how standard computer monitors emit a grotesque, hyper-saturated 450-nanometer blue wavelength. It ravages the melatonin receptors of the human eye. 

Naturally, the software industry's response to this biological reality is an abomination.

If you download an open-source blue light filter today, you are greeted by an **Electron bundle**:
* **350 MB of RAM** consumed by three separate Chromium child processes just to paint an amber square.
* **45 MB installer** accompanied by eight layers of automated telemetry reporting your keystrokes to an AWS bucket in us-east-1.
* A transparent layered window (`WS_EX_LAYERED`) that destroys desktop composition, causes input lag in high-refresh-rate monitors, and makes blacks look like dried mud.
* Maintained by people who use the word *"alignment"* unironically in sprint retrospectives.

I cannot tolerate inefficiency. It offends my sensibilities.

---

### The Solution: Anti-Retinazo

**Anti-Retinazo** does not negotiate with corporate bloat. It does not possess a splash screen. It does not ask for your email address. It does not contain analytics.

It communicates directly with the **Windows Graphics Device Interface (`gdi32.dll`)** via `SetDeviceGammaRamp`. It injects a pure, mathematically verified Look-Up Table (LUT) directly into your graphics adapter's DAC hardware. 

| Metric | Typical Corporate Utility | Anti-Retinazo |
| :--- | :--- | :--- |
| **Memory Footprint (RSS)** | 250 MB – 450 MB | **~12 to 14 MB** *(< 5 MB minimized)* |
| **CPU Utilization** | 1.2% – 4.5% continuous polling | **0.000%** *(Hardware GPU scanout)* |
| **Disk Overhead** | 80 MB+ Node runtime | **Zero dependencies** *(Standard library Python)* |
| **Overlay Artifacts** | Degrades FPS, intercepts mouse clicks | **None**. Native DAC hardware level |
| **Telemetry / Tracking** | Segment, Mixpanel, Datadog, Google Analytics | **Zero. Nada. Absolutely none.** |

---

### 🎛️ Operation & Controls

1. **One-Click Execution:**
   Double-click [`iniciar.bat`](iniciar.bat). It invokes `pythonw.exe` silently in the background. No unsightly command prompt window flashing across your tailored desktop wallpaper.
2. **Instant Binary Toggle:**
   The primary card provides a high-contrast switch: `[ ⏻ ACTIVAR FILTRO ]` $\leftrightarrow$ `[ ✓ FILTRO ACTIVO ]`. One click. Instantaneous transition.
3. **Continuous Real-Time Slider:**
   A seamless $0\% \to 100\%$ scale adjusting the color temperature from crisp daylight ($6500\text{ K}$) down to intimate candle-glow ($2400\text{ K}$).
4. **Discrete Presets:**
   * `☀️ Day (0%)` — Default factory calibration.
   * `🌤️ Afternoon (35%)` — Soft daylight filtering for sustained focus.
   * `🌙 Night (65%)` — Standard nocturnal eye-strain elimination.
   * `🕯️ Candle (85%)` — Deep amber tone for late-night hyperfocus sessions.
5. **Polite Lifecycle Teardown:**
   Closing the window (`X`) automatically restores your monitor's original calibration and saves your preferred intensity to `config.json`. If you want to keep the filter running silently with zero resource cost, simply **minimize the window (`_`)**.
6. **Emergency Reset:**
   If you ever kill the process with brute-force task managers, simply run [`restaurar_pantalla.bat`](restaurar_pantalla.bat). Your hardware LUT returns to standard linear curves within 20 milliseconds.

---
---

# 🇨🇱 Descripción en Español

### El Problema de la Mediocridad Corporativa

Al caer la noche, antes de revisar mis portafolios de inversión o ponerme a tocar líneas complejas de bajo, observo cómo los monitores convencionales vomitan una grotesca longitud de onda azul de 450 nanómetros que destruye las células ganglionares de la retina.

La respuesta de la industria del software a este problema fisiológico es una aberración digna de desprecio.

Cualquier filtro de pantalla promedio que encuentres hoy en internet viene empaquetado en **Electron**:
* **350 MB a 500 MB de RAM** desperdiciados en tres procesos aislados de Chromium sólo para mover un color.
* Un instalador inflado de 60 MB lleno de telemetría inútil para que un Product Manager justifique su sueldo en el próximo sprint.
* Una ventana transparente superpuesta (`WS_EX_LAYERED`) que te roba 20 FPS en cualquier juego, introduce latencia en el mouse y tiñe los negros con un tono a barro podrido.
* Hecho por gente que pasa más tiempo en ceremonias de Scrum y hablando de "cultura de empresa" que escribiendo código optimizado.

No tolero el código mediocre. Me parece una falta de respeto al silicio.

---

### La Solución: Anti-Retinazo

**Anti-Retinazo** no negocia con la basura corporativa. No tiene pantalla de carga, no te pide tu correo, no tiene telemetría y no necesita una sola dependencia externa de `npm` ni de `pip`.

Interactúa directo con la API nativa de **Windows GDI (`gdi32.dll`)** mediante `SetDeviceGammaRamp`. Le inyecta una matriz Look-Up Table (LUT) de 16-bit calculada matemáticamente directo al hardware de tu tarjeta gráfica.

| Métrica | La basura habitual de terceros | Anti-Retinazo |
| :--- | :--- | :--- |
| **Consumo de Memoria (RAM)** | 250 MB – 500 MB | **~12 a 14 MB** *(< 5 MB si lo minimizas)* |
| **Consumo de CPU** | 1.5% – 4% en segundo plano | **0.000%** *(El rasterizado lo hace la GPU)* |
| **Tamaño en Disco** | 100 MB con runtime de Node | **Cero dependencias** *(Python estándar)* |
| **Interferencia en Juegos** | Caída de FPS, tirones, clics perdidos | **Cero**. Modifica la LUT en hardware |
| **Telemetría y Rastreo** | Google Analytics, Sentry, Telemetry | **Cero. Absolutamente nada.** |

---

### 🎛️ Operación y Controles

1. **Lanzamiento Silencioso en 1 Clic:**
   Haz doble clic en [`iniciar.bat`](iniciar.bat). Se ejecuta directo a través de `pythonw.exe` sin mostrar ninguna ventana negra de consola.
2. **Switch Instantáneo:**
   Botón prominente de activación rápida: `[ ⏻ ACTIVAR FILTRO ]` $\leftrightarrow$ `[ ✓ FILTRO ACTIVO ]`. Un toque y cambia.
3. **Slider Continuo en Tiempo Real:**
   Control deslizante de $0\% \to 100\%$ que ajusta la calidez desde $6500\text{ K}$ (luz natural) hasta $2400\text{ K}$ (modo vela cálida) sin cortes ni retrasos.
4. **Perfiles de 1 Toque:**
   * `☀️ Día (0%)` — Calibración neutral limpia.
   * `🌤️ Tarde (35%)` — Filtro suave para largas jornadas de lectura o código.
   * `🌙 Noche (65%)` — Modo noche para no fatigar la vista.
   * `🕯️ Velas (85%)` — Ámbar profundo anti-insomnio para trabajar de madrugada.
5. **Cierre Impecable:**
   Al cerrar la ventana (`X`), el programa guarda tu preferencia en `config.json` y restaura automáticamente el monitor a su color original. Si quieres dejarlo activo de fondo sin que gaste nada, **solo minimiza la ventana (`_`)**.
6. **Reset de Emergencia:**
   Si cierras el proceso a la fuerza con el Administrador de Tareas, haz doble clic en [`restaurar_pantalla.bat`](restaurar_pantalla.bat) y la LUT de tu tarjeta gráfica volverá a 6500K en menos de 20 milisegundos.

---

## 📜 Licencia / License

MIT License. Copyright (c) 2026 Hans Soriano.

Haz lo que quieras con el código. La única condición moral es que jamás lo conviertas en una aplicación de Electron.
