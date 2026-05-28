<!-- README.md — CronometroAytoEspartinas · Iván Batista Herrero -->

<div align="center">

```
╔══════════════════════════════════════════════════════════╗
║  pleno ordinario · Ayuntamiento de Espartinas            ║
║  ┌──────────────────────────────────────────────────┐    ║
║  │ PSOE    05:42  ▓▓▓▓▓░  en curso                 │    ║
║  │ PP      02:11  ▓▓▒░░░  en curso                 │    ║
║  │ VOX     00:00  ██████  EXCEDIDO  +00:12         │    ║
║  │ POR_A   04:00  ░░░░░░  en espera                │    ║
║  └──────────────────────────────────────────────────┘    ║
╚══════════════════════════════════════════════════════════╝
```

# CRONÓMETRO DE PLENOS

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=111111)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-GUI-41CD52?style=for-the-badge&logo=qt&logoColor=white&labelColor=111111)](https://pypi.org/project/PyQt6/)
[![Estado](https://img.shields.io/badge/ESTADO-EN_PRODUCCIÓN-1affe4?style=for-the-badge&labelColor=111111)]()
[![Cliente](https://img.shields.io/badge/CLIENTE-Ayto._Espartinas-e63946?style=for-the-badge&labelColor=111111)]()

</div>

---

```bash
# Aplicación de escritorio para gestionar los tiempos de intervención
# de los grupos políticos durante los plenos municipales.
# Desarrollada durante las prácticas DAM en el Ayuntamiento de Espartinas.

ivan@shell:~$ python main.py
  cliente   →  Ayuntamiento de Espartinas (Sevilla)
  periodo   →  mar–jun 2025 · prácticas DAM
  stack     →  Python · PyQt6 · pygame · JSON
  patrón    →  MVC (Model – View – Controller)
```

---

## Descripción

Aplicación de escritorio desarrollada para el **Ayuntamiento de Espartinas** con el objetivo de controlar los tiempos de intervención de los grupos políticos durante los plenos municipales.

El sistema opera con **dos ventanas simultáneas**:

- **Visualización** — pantalla completa (proyector/TV de sala) con display LED por grupo político
- **Control** — panel del operador con botones Play/Stop/Reset y atajos de teclado

Soporta dos tipos de sesión: **pleno ordinario** y **pleno extraordinario**, con configuraciones independientes y persistencia en JSON.

---

## Características

- Cronómetros independientes por grupo político con logo de partido
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
├── main.py                        ← Entry point (QApplication)
│
├── controllers/
│   └── cronometro_app.py          ← QMainWindow principal (lógica central)
│
├── models/
│   ├── cronometro.py              ← Modelo de datos del cronómetro
│   └── almacenamiento.py          ← Persistencia JSON (carga/guarda)
│
├── views/
│   ├── vista_inicio.py            ← Pantalla de bienvenida
│   ├── vista_dividida.py          ← Panel de administración (CRUD timers)
│   ├── visualizacion.py           ← Display fullscreen (proyector)
│   ├── ventana_controles.py       ← Panel del operador (play/stop/reset)
│   ├── guia.py                    ← Ventana de ayuda
│   └── info.py                    ← Ventana de información
│
├── widgets/
│   └── auto_font_label.py         ← Label con fuente auto-escalable
│
├── assets/                        ← Fuentes DS-DIGI, iconos, audio
├── logos/                         ← Logos de grupos políticos
├── cronometros_ordinario.json     ← Config pleno ordinario
└── cronometros_extraordinario.json← Config pleno extraordinario
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

---

## Autor

**Iván Batista Herrero** — Técnico en DAM · prácticas en Ayuntamiento de Espartinas (mar–jun 2025)

[![Portfolio](https://img.shields.io/badge/Portfolio-ivanbatista.pages.dev-1affe4?style=flat-square&labelColor=111111)](https://ivanbatista.pages.dev)
[![Email](https://img.shields.io/badge/Email-ivanbatistah%40gmail.com-1affe4?style=flat-square&labelColor=111111)](mailto:ivanbatistah@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-1van106-1affe4?style=flat-square&logo=github&logoColor=white&labelColor=111111)](https://github.com/1van106)
