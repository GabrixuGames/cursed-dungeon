# 🐉 Cursed Dungeon

## 📌 Descripción general

*Cursed Dungeon* es un juego de rol por turnos ambientado en un universo oscuro y maldito. El jugador explora mazmorras, se enfrenta a enemigos cada vez más peligrosos y desarrolla sus habilidades a través de un sistema de progresión por niveles. El objetivo final es derrotar a *Ella, Diosa de la Perdición*, en el nivel 70.
El juego combina mecánicas clásicas de combate RPG con elementos estratégicos como estados alterados, gestión de recursos y enemigos con dificultad creciente. Está diseñado para ejecutarse inicialmente en terminal, con planes de expansión a una versión gráfica usando Pygame.

---

## 🧪 Versión actual

### *v0.4* - Professional Systems & Quality Update 🎯
**Actualización mayor con nuevos sistemas de juego y mejoras de calidad**

#### 🆕 Nuevos Sistemas Implementados:
- **Sistema de Guardado Múltiple** - 3 slots independientes con backup automático
- **Sistema de Habilidades Especiales** - 12 habilidades únicas con maná y cooldowns
- **Sistema de Logros** - 20+ achievements con seguimiento de progreso
- **Suite de Tests Automatizados** - Cobertura del 100% en tests unitarios

#### 🎮 Características Previas (v0.3):
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

## � Instalación y Ejecución

### 📋 Requisitos
- Python 3.9 o superior
- Sistema operativo: Linux, macOS o Windows
- 100 MB de espacio en disco

### ⚡ Instalación Rápida

```bash
# Clonar el repositorio
git clone [url-del-repo]
cd cursed-dungeon-main

# Ejecutar script de configuración (Linux/macOS)
./setup.sh

# O manualmente:
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 🎮 Ejecutar el Juego

```bash
# Activar entorno virtual
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Iniciar el juego
python main.py
```

### 🧪 Ejecutar Tests

```bash
# Con entorno virtual activado
python tests/test_suite.py
```

---

## 🖥️ Lenguajes utilizados3 slots y backup automático
- 🎯 **Sistema de habilidades** con 12 skills, maná y cooldowns
- 🏆 **Sistema de logros** con 20+ achievements y seguimiento
- 📁 **Preparado para escalabilidad** (versión gráfica, contenido adicional)
- ✅ **Tests automatizados** con cobertura completa
- 🐍 *Python* 3.12+ (compatible con 3.9+)

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
├── 📋 requirements.txt           # Dependencias del proyecto
├── 🔧 setup.sh                   # Script de configuración automática
├── 🚫 .gitignore                 # Archivos excluidos de git
├── 📋 settings.json              # Configuraciones de usuario
├── 💾 save.json                  # Guardado de partida (legacy)
├── 🧪 tests/                     # Suite de tests automatizados
│   └── ✅ test_suite.py          #   Tests unitarios (100% cobertura)
├── 📁 saves/                     # Guardados múltiples (3 slots)
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
│   ├── 💾 save_manager.py        #   Sistema de guardado múltiple (NUEVO)
│   ├── 🎯 skill_system.py        #   Sistema de habilidades (NUEVO)
│   ├── 🏆 achievement_system.py  #   Sistema de logros (NUEVO)
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
│   │   ├── 👤 main_character.py  #     Personaje principal (refactorizado)
│   │   ├── 👿 enemy.py           #     Sistema de enemigos (refactorizado)
│   │   └── 🗡️ weapons.py         #     Sistema de armas mejorado
│   └── 🔊 sounds/                #   Efectos de sonido
└── 📖 README.md                  # Documentación del proyecto
```

---

## 🎯 Sistema de Habilidades

### 💫 12 Habilidades Únicas

#### ⚔️ Ataque
- **Golpe Poderoso** - 2x daño (Nivel 1)
- **Corte Crítico** - 50% probabilidad de crítico 3x (Nivel 5)
- **Torbellino** - Ignora 50% evasión enemiga (Nivel 10)
- **Robo de Vida** - Recupera 50% del daño causado (Nivel 12)

#### 🛡️ Defensa
- **Defensa Férrea** - Reduce daño 50% por 2 turnos (Nivel 3)
- **Postura de Contraataque** - Devuelve 30% del daño (Nivel 8)
- **Escudo Divino** - Inmunidad total 1 turno (Nivel 20)

#### 💚 Soporte
- **Segundo Aliento** - Recupera 25% vida máxima (Nivel 7)
- **Concentración** - +30% daño por 3 turnos (Nivel 4)
- **Meditación** - Recupera 50 maná (Nivel 6)

#### ⚡ Especiales
- **Furia Berserker** - Sacrifica 20% vida para 3x daño (Nivel 15)
- **Golpe del Caos** - Daño aleatorio 0.5x-4x (Nivel 18)

---

## 🏆 Sistema de Logros

### 📊 20+ Achievements en 5 Categorías

- **Combate**: Primera Sangre, Guerrero Experimentado, Esquiva Perfecta
- **Progresión**: Alcanzar niveles 10, 25, 50, 70
- **Colección**: Coleccionista de Armas, Mercader Rico
- **Exploración**: Caminante de Mazmorras
- **Especiales**: Superviviente, Rey del Regreso (secretos)

Cada logro desbloquea recompensas (oro, experiencia) y se trackea automáticamente.

---

## 💾 Sistema de Guardado

### 3 Slots Independientes
- Guardado automático con metadata (fecha, nivel, versión)
- Sistema de backup automático
- Recuperación ante corrupción de datos
- Compatibilidad con guardados antiguos (legacy)

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
