# 🐉 Cursed Dungeon

## 📌 Descripción general

*Cursed Dungeon* es un juego de rol por turnos ambientado en un universo oscuro y maldito. El jugador explora mazmorras, se enfrenta a enemigos cada vez más peligrosos y desarrolla sus habilidades a través de un sistema de progresión por niveles. El objetivo final es derrotar a *Ella, Diosa de la Perdición*, en el nivel 70.
El juego combina mecánicas clásicas de combate RPG con elementos estratégicos como estados alterados, gestión de recursos y enemigos con dificultad creciente. Está diseñado para ejecutarse inicialmente en terminal, con planes de expansión a una versión gráfica usando Pygame.

---

## 🧪 Versión actual

### *v0.3* - Major Game Improvements & Refactoring 🚀
**Actualización completa del sistema de juego con mejoras visuales y arquitectónicas**

#### 🎮 Nuevas características:
- **Sistema de configuración centralizada** - Configuración unificada en `config.py`
- **Gestor de configuraciones de usuario** - Personalización de audio, display y controles
- **Sistema avanzado de gestión de pantalla** - Mejor renderizado y efectos visuales
- **Gestor de entrada mejorado** - Controles más responsivos y configurables
- **Sistema de subida de nivel refactorizado** - Progresión más fluida y balanceada

#### 🔧 Mejoras de código:
- **Refactorización completa del personaje principal** - Código más limpio y mantenible
- **Sistema de armas mejorado** - Mejor manejo de errores y validación de datos
- **Menú principal expandido** - Nuevas opciones y mejor navegación
- **Tienda rediseñada** - UI completamente renovada con mejor experiencia de usuario
- **Sistema de animaciones expandido** - Nuevas animaciones más fluidas y dinámicas

#### 🎨 Mejoras visuales:
- **Fondo de mazmorra dinámico** - Elementos animados como antorchas y gotas de agua
- **Efectos visuales avanzados** - Sistema de fade in/out para transiciones suaves
- **Renderizado de texto mejorado** - Mejor legibilidad y presentación
- **Nuevas fuentes tipográficas** - Tipografías modernas para mejor experiencia visual

#### 📁 Restructuración del código:
- **Modularización avanzada** - Mejor separación de responsabilidades
- **Sistema robusto de manejo de errores** - Validación y respaldo automático
- **Archivos obsoletos eliminados** - Limpieza del código base
- **Nueva organización de assets** - Estructura preparada para contenido gráfico

#### 📊 Estadísticas de la actualización:
- **46 archivos modificados**
- **3,542 líneas agregadas**
- **634 líneas eliminadas**

---

### *v0.2* - Base funcional
Incluye: sistema de combate funcional, enemigos con estados alterados, animaciones básicas en terminal, y primeras pruebas con estructura modular.

---

## 🖥️ Lenguajes utilizados

- 🐍 *Python* 3.9+

---

## 🧰 Librerías y frameworks

### 🎨 Renderizado y UI:
- **pygame** – Sistema de renderizado, efectos visuales y gestión de pantalla
- **asciimatics** – Animaciones por terminal (compatible con versión anterior)

### 🗃️ Gestión de datos:
- **json** – Configuración, guardado de partidas y bases de datos
- **os** – Gestión de archivos y rutas del sistema

### 🔧 Utilidades estándar:
- **time** – Manejo de tiempos y delays en animaciones
- **random** – Generación de eventos aleatorios en combate
- **math** – Cálculos de balanceo y progresión

---

## ✨ Características del proyecto

### 🎮 Gameplay Core:
- ⚔️ **Combate por turnos** con animaciones de ataque y efectos dinámicos
- 📈 **Sistema de progresión** hasta nivel 70 con balanceo mejorado
- 👿 **Jefes únicos** con habilidades especiales y mecánicas avanzadas
- 🧪 **Estados alterados** con probabilidades dinámicas según tipo de enemigo
- 🛍️ **Sistema de tienda** completamente rediseñado con mejor experiencia

### 🎨 Experiencia Visual:
- 🎬 **Animaciones fluidas** con sistema expandido de efectos
- 🏰 **Fondo dinámico** con elementos animados (antorchas, gotas de agua)
- ✨ **Efectos visuales** avanzados con transiciones fade in/out
- 🔤 **Tipografías modernas** para mejor legibilidad

### ⚙️ Arquitectura Técnica:
- 🧱 **Estructura modular** con separación clara de responsabilidades
- 📋 **Sistema de configuración** centralizada y personalizable
- 🎮 **Gestión avanzada de entrada** con controles configurables
- 💾 **Sistema robusto de guardado** con validación y respaldo automático
- 📁 **Preparado para escalabilidad** (versión gráfica, contenido adicional)

---

## 🗂️ Estructura del proyecto

```plaintext
cursed-dungeon/
├── 🚀 config.py                  # Configuración centralizada del juego
├── 🎮 main.py                    # Punto de entrada principal
├── 📋 settings.json              # Configuraciones de usuario
├── 🎲 levels/                    # Niveles y sistemas de juego
│   ├── ⚔️ dungeon_combat.py      #   Sistema de combate en mazmorras
│   ├── 📱 game_menu.py           #   Menú principal expandido
│   ├── 📈 level_up.py            #   Sistema de progresión refactorizado
│   ├── 🛍️ shop.py                #   Tienda rediseñada
│   └── 🎯 start_game.py          #   Inicialización del juego
├── 💻 src/                       # Código fuente principal
│   ├── 🖥️ display_manager.py     #   Gestión de pantalla y renderizado
│   ├── 🎮 input_manager.py       #   Gestión avanzada de entrada
│   ├── 🔧 others.py              #   Utilidades y funciones auxiliares
│   ├── ⚙️ settings_manager.py    #   Gestión de configuraciones
│   ├── 🎬 animations/            #   Sistema de animaciones
│   │   ├── 🎭 animations.py      #     Animaciones principales
│   │   ├── ✨ new_animations.py  #     Nuevas animaciones avanzadas
│   │   └── 🚶 walking.py         #     Animaciones de movimiento
│   ├── 🎨 assets/                #   Recursos del juego
│   │   └── 🔤 fonts/             #     Fuentes tipográficas
│   ├── 📊 db/                    #   Bases de datos del juego
│   │   ├── 👾 enemyDb.json       #     Datos de enemigos
│   │   └── ⚔️ weaponsDb.json     #     Datos de armas
│   ├── 🎯 object/                #   Clases principales
│   │   ├── 👤 main_character.py  #     Personaje principal refactorizado
│   │   ├── 👿 enemy.py           #     Sistema de enemigos
│   │   └── 🗡️ weapons.py         #     Sistema de armas mejorado
│   └── 🔊 sounds/                #   Efectos de sonido
└── 📖 README.md                  # Documentación del proyecto
```

---

## 🎯 Próximas versiones

### 🔮 v0.4 - Planificado:
- 🎮 Sistema de sprites y gráficos 2D 
- 🔊 Integración completa de audio
- 🌍 Nuevas mazmorras y contenido
- 🎨 Mejoras adicionales de UI/UX

```plaintext
Cursed-Dungeon/
├── data/           # Configuración de enemigos, niveles, estados, etc.
├── engine/         # Lógica del juego: combate, gestión de turnos, etc.
├── animations/     # Animaciones y efectos visuales en terminal
├── assets/         # Archivos visuales o sonoros (planeado para el futuro)
├── main.py         # Punto de entrada del juego
└── README.md       # Este archivo con la documentació
