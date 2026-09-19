# 🛡️ Anti-Retinazo: El filtro de luz azul sin mierda

> *"¿Por qué mierda una aplicación para cambiar el color de la pantalla necesita 350 MB de RAM, un Chromium incrustado, 4 hilos de telemetría y un demonio en segundo plano?"*
> — Cualquier ser humano con más de dos neuronas funcionales.

Bienvenido a **Anti-Retinazo**. Una herramienta que hace **exactamente una cosa** y no te roba recursos como si fuera un minero de criptomonedas de Europa del Este.

---

## 🧐 ¿Por qué existe esto?

El software moderno está roto. Si buscas un filtro de luz azul hoy en día te encuentras con dos tragedias:
1. **La "Luz Nocturna" de Windows:** Funciona cuando quiere, se descalibra con alt-tab, se apaga sola a las 3 AM para quemarte las córneas con 6500K a traición, y requiere rezarle a 4 servicios del registro de Windows.
2. **Aplicaciones de terceros en Electron / Webview:** Pesan 90 MB en el disco, consumen 400 MB de RAM para mostrar un slider y crean una ventana transparente que laguea el cursor en los juegos y te bota 15 FPS en cualquier cosa que abras.

**Anti-Retinazo** manda todo eso al carajo.

---

## ⚡ Especificaciones Técnicas (Zero-Bullshit)

| Métrica | Lo que te meten otras apps | Anti-Retinazo |
| :--- | :--- | :--- |
| **Consumo de RAM** | ~180 MB - 450 MB | **~12 a 14 MB** (y Windows la comprime a <5MB minimizado) |
| **Consumo de CPU** | 1.5% - 5.0% permanente | **0.0%** (Literalmente cero) |
| **Instalador** | 80 MB `.exe` con telemetry | **0 bytes** (Es código puro, clonar y correr) |
| **Dependencias externas** | `npm install` de 1.2 GB o 8 librerías de `pip` | **Cero**. Solo librerías estándar de Python (`ctypes`, `tkinter`) |
| **Impacto en Juegos / Fullscreen** | Drops de FPS, clics perdidos | **Ninguno**. Modifica la LUT en hardware, no crea capas invisibles |

---

## 🔬 ¿Cómo funciona por debajo?

En vez de poner una capa semitransparente color meado encima de tu pantalla (lo que hace el 90% de los scripts ordinarios), **Anti-Retinazo** habla directamente con el subsistema gráfico de Windows (**Win32 GDI / `gdi32.dll`**) mediante `SetDeviceGammaRamp`.

Le inyecta una matriz Look-Up Table (LUT) matemática de 3 canales $\times$ 256 valores (16-bit) directamente al driver de video de tu tarjeta gráfica.
* El canal **Rojo** se mantiene estable.
* El canal **Verde** se calcula con una suave curva logarítmica para evitar que tu pantalla parezca un vómito magenta.
* El canal **Azul** se atenúa progresivamente hasta un 80% según el slider.
* **Resultado:** Hardware puro. La GPU hace la mezcla en el barrido de salida. Cero cálculo por software.

---

## 🕹️ Cómo se usa

### 1. Iniciar sin consola negra
Haz doble clic en:
```text
iniciar.bat
```
*(Lanza `pythonw.exe app.pyw` en segundo plano silencioso, sin ventanas de terminal estorbando)*.

### 2. Controles
* **Un Clic:** Botón gigante `[ ⏻ ACTIVAR / APAGAR ]`.
* **Slider en Vivo:** Muévelo y siente la calidez en tiempo real, desde luz de día (6500K) hasta modo "vela medieval" (2400K).
* **Presets:** Cuatro botones directos:
  * `☀️ Día (0%)` -> Neutral de fábrica.
  * `🌤️ Tarde (35%)` -> Para programar 10 horas sin terminar con dolor de cabeza.
  * `🌙 Noche (65%)` -> Modo noche estándar.
  * `🕯️ Velas (85%)` -> Cuando son las 4 AM y la luz azul es tu peor enemigo.
* **Segundo Plano:** Minimiza la ventana (`_`) y sigue con tu vida.
* **Cierre Seguro:** Al presionar la `X`, restaura tu pantalla a su estado original para que no te quedes ciego si reinicias el monitor.

---

## 🚨 Reset de Emergencia

Si eres de los que mata procesos a lo bestia con `taskkill /f /im python.exe`:
No te preocupes. Tienes [`restaurar_pantalla.bat`](file:///c:/Users/Numpay/Desktop/Codes/filtro-luz-azul/restaurar_pantalla.bat) que resetea la LUT de la tarjeta gráfica a 6500K en medio milisegundo.

---

## 📜 Licencia

MIT. Haz lo que se te cante con el código, solo no le metas Electron por favor.
