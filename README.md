<!-- README.md — CronometroAytoEspartinas -->

<div align="center">

<br/>

<img src="assets/logo_espartinas.png" alt="Ayuntamiento de Espartinas" width="200"/>

<br/><br/>

# CRONÓMETRO DE PLENOS

**Gestión de tiempos de intervención para sesiones plenarias municipales**

<br/>

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=1a1a2e)
![PyQt6](https://img.shields.io/badge/PyQt6-6.4+-41CD52?style=for-the-badge&logo=qt&logoColor=white&labelColor=1a1a2e)
![pygame](https://img.shields.io/badge/pygame-audio-e07a00?style=for-the-badge&labelColor=1a1a2e)
![JSON](https://img.shields.io/badge/JSON-persistencia-4a90a4?style=for-the-badge&labelColor=1a1a2e)

![Estado](https://img.shields.io/badge/ESTADO-ENTREGADO-2a9d8f?style=for-the-badge&labelColor=1a1a2e)
![Patrón](https://img.shields.io/badge/ARQUITECTURA-MVC-6b4c9a?style=for-the-badge&labelColor=1a1a2e)
![Periodo](https://img.shields.io/badge/PERIODO-mar–jun_2025-5a7a9a?style=for-the-badge&labelColor=1a1a2e)

<br/>

```
  pleno ordinario
  +--------------------------------------------------------+
  |                                                        |
  |   GRUPO A    [==========---------]   05:42   en curso  |
  |   GRUPO B    [======-------------]   02:11   en curso  |
  |   GRUPO C    [===================]   00:00   EXCEDIDO  |
  |   GRUPO D    [-------------------]   04:00   en espera |
  |                                                        |
  +--------------------------------------------------------+
  [pantalla completa / proyector]   [panel / operador]
```

</div>

<br/>

---

## `//` Descripción

Aplicación de escritorio en **Python** con arquitectura **MVC** para gestionar los tiempos de intervención de los grupos políticos durante los plenos municipales.

El sistema opera con **dos ventanas simultáneas** pensadas para dos pantallas distintas:

| Ventana | Destino | Función |
|---|---|---|
| **Visualización** | Proyector / pantalla de sala | Display LED fullscreen con el tiempo de cada grupo |
| **Control** | Monitor del operador | Panel con Play · Stop · Reset y atajos de teclado |

Soporta dos tipos de sesión — **pleno ordinario** y **pleno extraordinario** — con configuraciones independientes persistidas en JSON.

<br/>

---

## `//` Características

<br/>

**Gestión de tiempos**

![Cuenta atrás](https://img.shields.io/badge/-Cuenta_atrás_por_grupo-2a9d8f?style=flat-square&labelColor=1a1a2e)
![Overtime](https://img.shields.io/badge/-Paso_automático_a_tiempo_excedido-e63946?style=flat-square&labelColor=1a1a2e)
![Alarma](https://img.shields.io/badge/-Alarma_sonora_al_llegar_a_00:00-e07a00?style=flat-square&labelColor=1a1a2e)
![Cascada](https://img.shields.io/badge/-Sincronización_en_cascada_entre_turnos-6b4c9a?style=flat-square&labelColor=1a1a2e)

**Interfaz**

![Logos](https://img.shields.io/badge/-Logo_personalizable_por_grupo-4a90a4?style=flat-square&labelColor=1a1a2e)
![Drag](https://img.shields.io/badge/-Reordenamiento_por_arrastrar_y_soltar-5a7a9a?style=flat-square&labelColor=1a1a2e)
![LED](https://img.shields.io/badge/-Display_con_fuente_LED_(DS--DIGI)-2a9d8f?style=flat-square&labelColor=1a1a2e)

**Productividad**

![Atajos](https://img.shields.io/badge/-Atajos_de_teclado_1–9_toggle_·_Ctrl+1–9_reset-4a90a4?style=flat-square&labelColor=1a1a2e)
![Persistencia](https://img.shields.io/badge/-Configuración_persistente_en_JSON-5a7a9a?style=flat-square&labelColor=1a1a2e)
![Sesiones](https://img.shields.io/badge/-Plenos_ordinarios_y_extraordinarios-6b4c9a?style=flat-square&labelColor=1a1a2e)

<br/>

---

## `//` Arquitectura

```
CronometroAytoEspartinas/
│
├── main.py                          ←  Entry point · QApplication
│
├── controllers/
│   └── cronometro_app.py            ←  QMainWindow · lógica central
│
├── models/
│   ├── cronometro.py                ←  Modelo de datos del cronómetro
│   └── almacenamiento.py            ←  Carga y guarda JSON
│
├── views/
│   ├── vista_inicio.py              ←  Pantalla de bienvenida
│   ├── vista_dividida.py            ←  Admin: añadir / editar / ordenar
│   ├── visualizacion.py             ←  Display fullscreen (proyector)
│   ├── ventana_controles.py         ←  Panel del operador
│   ├── guia.py                      ←  Ayuda
│   └── info.py                      ←  Información de la app
│
├── widgets/
│   └── auto_font_label.py           ←  Label con fuente auto-escalable
│
├── assets/                          ←  Fuentes DS-DIGI · iconos · audio
├── logos/                           ←  Logos de grupos
├── cronometros_ordinario.json       ←  Config pleno ordinario
└── cronometros_extraordinario.json  ←  Config pleno extraordinario
```

<br/>

---

## `//` Flujo de uso

```
  ┌─[ ADMIN ]──────────────────────────────────────────────────────┐
  │  Menú Admin → Pleno Ordinario / Extraordinario                 │
  │  └── Configurar grupos: nombre · tiempo · logo · orden         │
  └────────────────────────────────────────────────────────────────┘
                              │
                              ▼
  ┌─[ SESIÓN ]─────────────────────────────────────────────────────┐
  │  Menú Visualización → Ver Pleno                                │
  │  ├── [Proyector]   VentanaVisualizacion  ·  fullscreen LED     │
  │  └── [Operador]    VentanaControles      ·  Play · Stop · Reset│
  └────────────────────────────────────────────────────────────────┘
                              │
                              ▼
  ┌─[ DURANTE EL PLENO ]───────────────────────────────────────────┐
  │  Tecla [1–9]       →  toggle play / stop del cronómetro        │
  │  Tecla [Ctrl+1–9]  →  reset del cronómetro                     │
  │  00:00             →  alarma sonora · paso a tiempo excedido   │
  │  Tiempo excedido   →  display en rojo · cuenta ascendente      │
  └────────────────────────────────────────────────────────────────┘
```

<br/>

---

## `//` Estados visuales

<div align="center">

| | Estado | Display | Descripción |
|:---:|---|---|---|
| ![](https://img.shields.io/badge/_%20_-E0E0E0?style=flat-square) | **En espera** | Gris `#E0E0E0` | Cronómetro configurado, no iniciado |
| ![](https://img.shields.io/badge/_%20_-F5F5F5?style=flat-square) | **En curso** | Blanco `#F5F5F5` | Cuenta atrás activa |
| ![](https://img.shields.io/badge/_%20_-FF6B6B?style=flat-square) | **Excedido** | Rojo `#FF6B6B` | Tiempo agotado · cuenta ascendente |

</div>

<br/>

---

## `//` Instalación y ejecución

**Requisitos**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white&labelColor=1a1a2e)
![PyQt6](https://img.shields.io/badge/PyQt6-6.4+-41CD52?style=flat-square&logo=qt&logoColor=white&labelColor=1a1a2e)
![pygame](https://img.shields.io/badge/pygame-2.0+-e07a00?style=flat-square&labelColor=1a1a2e)

```bash
git clone https://github.com/1van106/CronometoAytoEspartinas.git
cd CronometoAytoEspartinas
pip install PyQt6 pygame
python main.py
```
