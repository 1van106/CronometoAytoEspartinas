<!-- README.md — CronometroAytoEspartinas -->

<div align="center">

<img src="assets/logo_espartinas.png" alt="Logo" width="200"/>

```
╔══════════════════════════════════════════════════════════╗
║  pleno ordinario                                         ║
║  ┌──────────────────────────────────────────────────┐    ║
║  │ GRUPO A   05:42  ▓▓▓▓▓░  en curso               │    ║
║  │ GRUPO B   02:11  ▓▓▒░░░  en curso               │    ║
║  │ GRUPO C   00:00  ██████  EXCEDIDO  +00:12       │    ║
║  │ GRUPO D   04:00  ░░░░░░  en espera              │    ║
║  └──────────────────────────────────────────────────┘    ║
╚══════════════════════════════════════════════════════════╝
```

# CRONÓMETRO DE PLENOS

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=111111)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-GUI-41CD52?style=for-the-badge&logo=qt&logoColor=white&labelColor=111111)](https://pypi.org/project/PyQt6/)
[![Estado](https://img.shields.io/badge/ESTADO-ENTREGADO-1affe4?style=for-the-badge&labelColor=111111)]()

</div>

---

```
# Aplicación de escritorio para gestionar los tiempos de intervención
# de los grupos políticos durante los plenos municipales.

  stack     →  Python · PyQt6 · pygame · JSON
  patrón    →  MVC (Model – View – Controller)
  periodo   →  mar–jun 2025
```

---

## Descripción

Aplicación de escritorio para controlar los tiempos de intervención de los grupos políticos durante los plenos municipales.

El sistema opera con **dos ventanas simultáneas**:

- **Visualización** — pantalla completa (proyector/TV de sala) con display LED por grupo
- **Control** — panel del operador con botones Play/Stop/Reset y atajos de teclado

Soporta dos tipos de sesión: **pleno ordinario** y **pleno extraordinario**, con configuraciones independientes y persistencia en JSON.

---

## Características

- Cronómetros independientes por grupo con logo personalizable
- Cuenta atrás con alarma sonora al llegar a `00:00` (pygame)
- Paso automático a **tiempo excedido** (cuenta hacia adelante en rojo)
- **Sincronización en cascada**: al expirar un turno, se inician automáticamente los turnos secundarios de menor duración del mismo grupo
- Reordenamiento manual de cronómetros por arrastrar y soltar
- Atajos de teclado: `1–9` toggle play/stop · `Ctrl+1–9` reset
- Configuración persistente en JSON entre sesiones
- Soporte para plenos **ordinarios** y **extraordinarios**

---

## Arquitectura

```
CronometroAytoEspartinas/
├── main.py                         ← Entry point (QApplication)
│
├── controllers/
│   └── cronometro_app.py           ← QMainWindow principal (lógica central)
│
├── models/
│   ├── cronometro.py               ← Modelo de datos del cronómetro
│   └── almacenamiento.py           ← Persistencia JSON (carga/guarda)
│
├── views/
│   ├── vista_inicio.py             ← Pantalla de bienvenida
│   ├── vista_dividida.py           ← Panel de administración (CRUD timers)
│   ├── visualizacion.py            ← Display fullscreen (proyector)
│   ├── ventana_controles.py        ← Panel del operador (play/stop/reset)
│   ├── guia.py                     ← Ventana de ayuda
│   └── info.py                     ← Ventana de información
│
├── widgets/
│   └── auto_font_label.py          ← Label con fuente auto-escalable
│
├── assets/                         ← Fuentes DS-DIGI, iconos, audio
├── logos/                          ← Logos de grupos
├── cronometros_ordinario.json      ← Config pleno ordinario
└── cronometros_extraordinario.json ← Config pleno extraordinario
```

---

## Flujo de uso

```
1. Menú Admin → Pleno Ordinario / Extraordinario
      └── Configurar grupos: nombre, tiempo, logo, orden

2. Menú Visualización → Ver Pleno
      ├── [Proyector]  VentanaVisualizacion  — fullscreen, fuente LED
      └── [Operador]   VentanaControles      — Play · Stop · Reset

3. Durante el pleno:
      ├── Tecla [1-9]        → toggle play/stop del cronómetro
      ├── Tecla [Ctrl+1-9]   → reset del cronómetro
      ├── 00:00              → alarma sonora + paso a tiempo excedido
      └── Tiempo excedido    → display en rojo + cuenta ascendente
```

---

## Requisitos

```bash
pip install PyQt6 pygame
```

| Dependencia | Versión mínima | Uso |
|---|---|---|
| Python | 3.11+ | Runtime |
| PyQt6 | 6.4+ | Interfaz gráfica |
| pygame | 2.0+ | Alarma sonora |

---

## Ejecución

```bash
git clone https://github.com/1van106/CronometoAytoEspartinas.git
cd CronometoAytoEspartinas
pip install PyQt6 pygame
python main.py
```

---

## Estados del cronómetro

| Estado | Color | Descripción |
|---|---|---|
| En espera | Gris `#E0E0E0` | Cronómetro configurado, no iniciado |
| En curso | Blanco `#F5F5F5` | Cuenta atrás activa |
| Excedido | Rojo `#FF6B6B` | Tiempo agotado, cuenta ascendente |
