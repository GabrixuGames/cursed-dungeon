# 📋 CHANGELOG

Todos los cambios notables del proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

---

## [0.5.4] - 2026-01-24

### 🧩 Ajustes UI/UX post FASE 7
- **ACTUALIZADO**: `levels/dungeon_combat.py` - UI inferior unificada y HP/MP solo texto
- **ACTUALIZADO**: `levels/combat_menu.py` - Menú y submenús dentro del mismo cuadro inferior
  - Columna derecha con descripción/potencia y truncado de textos largos
  - Tipografía consistente con logs y descripción más pequeña
  - Fix de selección en submenú (Enter ahora ejecuta skills/items)
- **ACTUALIZADO**: `src/others.py` - Opacidad consistente en `combat_message_box`

### 🔧 Soporte de inventario en combate
- **ACTUALIZADO**: `levels/dungeon_combat.py` - Carga de itemsDb garantizada al entrar en combate
- **ACTUALIZADO**: `main.py` - Ítems de prueba añadidos al cargar partida (overflow testing)

## [0.5.3] - 2026-01-24

### 🎮 FASE 6 y 7 COMPLETADAS: Integración y Testing

#### Sistema de Achievements Integrado (FASE 6.1)
- **ACTUALIZADO**: `src/object/main_character.py` - AchievementManager integrado
  - Sistema de tracking añadido con stats:
    - `enemies_defeated`: Contador de enemigos derrotados
    - `consecutive_dodges`: Esquivas consecutivas
    - `low_hp_kills`: Kills con <10% HP
    - `flawless_combats`: Combates sin daño recibido
    - `skills_used`, `items_used`, `flee_count`: Trackeo de acciones
    - `shop_visits`, `steps_walked`: Progreso general
  - Métodos de tracking:
    - `track_enemy_defeat()`: +1 enemigo, verifica logros
    - `track_dodge()`: +1 esquiva, progreso "Esquiva Perfecta"
    - `reset_dodge_streak()`: Reset al recibir daño
    - `track_flawless_combat()`: Victoria sin daño
    - `track_skill_use()`, `track_item_use()`, `track_flee()`: Contadores
    - `track_shop_visit()`: Progreso "Adicto a las Compras"
    - `track_level_up()`: Logros de nivel (10, 25, 50, 70)

- **ACTUALIZADO**: `levels/dungeon_combat.py` - Tracking integrado en combate
  - Victoria: `track_enemy_defeat()` + `track_flawless_combat()`
  - Huida: `track_flee()`
  - Esquivas: `track_dodge()` cuando esquiva, `reset_dodge_streak()` cuando recibe daño
  - Skills: `track_skill_use()` en `_use_skill()`
  - Items: `track_item_use()` en `_use_item()`

- **ACTUALIZADO**: `levels/shop.py` - `track_shop_visit()` al entrar

- **ACTUALIZADO**: `src/achievement_system.py` - Serialization
  - Añadidos `to_dict()` y `from_dict()` para save/load
  - Persiste: unlocked, unlock_date, progress

#### Save System Actualizado (FASE 6.2)
- **ACTUALIZADO**: `src/object/main_character.py` - `save_game()` y `load_game()`
  - **NUEVO**: Campo `stats` en save (todos los counters)
  - **NUEVO**: Campo `achievement_progress` (estado de achievements)
  - Backward compatible: loads antiguos inicializan stats vacíos
  - Restaura progreso de logros al cargar

#### Testing Completo (FASE 7.1)
- ✅ **23/23 tests pasando** (100% success rate)
  - test_suite.py: 10/10 ✅
  - test_items_inventory.py: 10/10 ✅
  - test_combat_system.py: 3/3 ✅
- Zero regressions
- Sistema de achievements no rompe funcionalidad existente

#### Balanceo Verificado (FASE 7.2)
- ✅ Precios de items balanceados:
  - HP Pociones: 25/50/100 oro (30/60/120 HP)
  - MP Pociones: 20/40/80 oro (20/40/80 MP)
  - Antídotos: 30 oro (cura estados)
  - Buffs: 50-100 oro (efectos temporales)
  - Items especiales: 200-300 oro (revival, escape)
- ✅ Probabilidad huida: 50% base + 5% por nivel (10-90% range)
- ✅ Costos de habilidades: 10-30 MP (balanceados con regeneración)
- ✅ Progreso de nivel: 100 * 1.2^(level-1) EXP

### 📊 Progreso
- **FASE 6**: 100% completada
- **FASE 7**: 100% completada  
- **Progreso total**: 95% (7/8 fases completadas)

---

## [0.5.2] - 2026-01-24

### 🎨 FASE 5 COMPLETADA: Mejoras de UI de Combate

#### Escena de Combate Mejorada
- **ACTUALIZADO**: `levels/dungeon_combat.py` - `draw_combat_scene()` completamente rediseñada
  - UI reposicionada más alta (NAME_Y=80, antes 170)
  - **NUEVA**: Barra de maná (MP) para el jugador (azul, 220x18px)
  - Barras de vida mejoradas: más anchas (220px), más altas (18px)
  - Colores dinámicos según HP: verde (>60%), amarillo (>30%), rojo (<30%)
  - Números de HP/MP visibles en las barras
  - Nivel del jugador mostrado junto al nombre
  - Mejor espaciado (BAR_SPACING=28)

#### Menú de Combate Mejorado
- **ACTUALIZADO**: `levels/combat_menu.py` - Diseño visual completamente renovado
  - Iconos emoji añadidos: ⚔ Atacar, ✨ Habilidad, 🎒 Item, 🏃 Huir
  - Menú más ancho (550px) y centrado
  - Fondo con mejor transparencia (220 alpha) y colores (20,20,30)
  - Borde brillante (100,100,150) con grosor 3px
  - Selección con fondo animado (80,80,120) y borde azul (150,200,255)
  - Color amarillo brillante (255,255,100) para opción seleccionada
  - Separadores verticales entre opciones (60,60,80)

#### Submenús Mejorados
- **ACTUALIZADO**: `levels/combat_menu.py` - `_draw_submenu()` rediseñado
  - Submenú más grande (600px ancho, hasta 450px alto)
  - Título con iconos: ✨ HABILIDADES / 🎒 ITEMS
  - Borde doble brillante para mejor apariencia
  - Fondo de selección con highlight (70,70,110)
  - Indicador mejorado: ► en lugar de >
  - Iconos de información: 💙 para MP, colores por estado
  - Información organizada: nombre a la izquierda, costo/cantidad a la derecha
  - Colores específicos:
    - Azul (100,150,255) para costo de maná
    - Rojo (150,100,100) para habilidades no disponibles
    - Verde (150,200,150) para cantidad de items

#### Combat Message Box
- **ACTUALIZADO**: `src/others.py` - Reposicionamiento de `combat_message_box`
  - `margin_bottom` cambiado de 80 a 150
  - `height` ajustado de 110 a 100
  - Posición optimizada para menú inferior en Y=530

### ✅ Tests
- **23/23 tests pasando** (100% success rate)
  - 10/10 test_suite.py
  - 10/10 test_items_inventory.py
  - 3/3 test_combat_system.py
- Sin errores de sintaxis
- Compatibilidad total con FASE 4

### 📊 Progreso
- **FASE 5**: 100% completada
- **Progreso total**: 90% (5/8 fases completadas)

---

## [0.5.1] - 2026-01-24

### 🤖 Mejoras del Sistema de Agentes
- **ACTUALIZADO**: `AGENTS.md` - PM ahora usa **Claude Sonnet 4** (modelo más potente)
  - PM es el rol más crítico: coordina todo el equipo
  - Toma las decisiones más importantes
  - Necesita el modelo más avanzado disponible

### �📚 Documentación - Corrección para ASCII Art

- **ACTUALIZADO**: `GAMEDEV_STANDARDS.md` - Enfoque completo en arte ASCII
  - Eliminadas referencias a sprites PNG y spritesheets
  - Añadidas secciones específicas para renderizado ASCII
  - Ejemplos de animaciones con caracteres
  - Sistema de partículas ASCII
  - UI con caracteres Unicode (┌─┐│└┘ █░)
  - Paletas de color para ASCII art
  - Best practices para fuentes monoespaciadas

- **ACTUALIZADO**: `RULES.md` - Gestión de assets para juegos ASCII
  - Filosofía visual clarificada: Arte ASCII únicamente
  - Estructura de assets sin sprites/imágenes
  - Nomenclatura para fuentes y audio
  - Arte ASCII definido en código Python
  - Control de versiones adaptado

- **ACTUALIZADO**: `DEVELOPMENT.md` - Sistema de animaciones ASCII
  - Sección de animaciones actualizada para ASCII art
  - Ejemplos basados en código real del proyecto
  - Uso de draw_character() y animation_player_attack()
  - Texto con efecto de escritura (slow_print)
  - UI con caracteres Unicode

### 📝 Notas
- **Aclaración importante**: Este proyecto usa **arte ASCII** para personajes y enemigos
- NO se usan sprites PNG ni imágenes bitmap
- Todas las animaciones son transiciones de frames ASCII
- Audio sí se utiliza (música y efectos de sonido)

---

## [0.5.0] - 2026-01-24

### 📚 Documentación
- **NUEVO**: `GAMEDEV_STANDARDS.md` - Estándares específicos de desarrollo con Pygame
  - Patrones de game loop (delta time, fixed timestep)
  - Optimización de rendering (dirty rects, surface caching)
  - State Machine pattern para gestión de estados
  - Sistema de partículas completo
  - Audio Manager con control de volumen
  - Sistema de animaciones multi-frame
  - Combat Calculator con tipos de daño
  - Status Effects Manager
  - FPS Counter y Debug Overlay
  - Best practices checklist

- **ACTUALIZADO**: `AGENTS.md` - Sistema de agentes mejorado
  - Añadidas métricas específicas por rol
  - Responsibilities detalladas para cada agente
  - Instrucciones expandidas para GameDev y QA
  - Énfasis en playtesting y balanceo
  - Métricas de performance y calidad

- **ACTUALIZADO**: `WORKFLOW.md` - Proceso ágil para game development
  - Simplificado para iteración rápida
  - Sprints de 1-2 semanas
  - Daily standups de 15 minutos
  - Playtesting sessions programadas
  - Prioridades específicas de juegos (diversión > funcionalidad)
  - Gestión de cambios por severidad
  - Release checklist detallado
  - Métricas de éxito por sprint

- **ACTUALIZADO**: `DEVELOPMENT.md` - Guía técnica expandida
  - Sección completa de Sistema de Animaciones
  - Sección de Sistema de Audio con AudioManager
  - Troubleshooting común con soluciones
  - Ejemplos de integración de mecánicas
  - Guía de deployment con PyInstaller
  - Snippets de código funcionales

- **ACTUALIZADO**: `RULES.md` - Normas del equipo mejoradas
  - Gestión específica de assets de juegos
  - Nomenclatura de sprites, sonidos y fuentes
  - Control de versiones de assets
  - Prioridades adaptadas a game development
  - Proceso de playtesting definido
  - Performance targets específicos (60 FPS)
  - Sistema de severidad de bugs
  - Procedimientos de escalación

- **NUEVO**: `AGENTS_GUIDE.md` - Guía de trabajo con el sistema de agentes
  - Introducción al equipo de agentes
  - Cómo solicitar trabajo a agentes específicos
  - Flujo típico de trabajo
  - Ejemplos de uso para features, bugs y optimización
  - Comandos rápidos para eficiencia
  - Estado actual del proyecto
  - Tips para máxima productividad

### 🎯 Mejoras de Proceso
- Sistema de agentes ahora especificado en todas las interacciones
- Workflow adaptado para desarrollo ágil de videojuegos
- Énfasis en playtesting y feedback rápido
- Documentación orientada específicamente a Pygame
- Estándares técnicos actualizados para juegos 2D

### 📝 Notas
- Toda la documentación actualizada a versión 0.5
- Sistema de agentes listo para uso en desarrollo continuo
- Base sólida para iteración rápida en desarrollo

---

## [0.4.0] - 2026-01-24

### 🆕 Añadido
- **Sistema de Guardado Múltiple**: 3 slots independientes con metadata
  - Backup automático antes de cada guardado
  - Recuperación desde backup si se detecta corrupción
  - Metadata: fecha, nivel, versión del juego
  - Clase `SaveManager` en `src/save_manager.py`
  
- **Sistema de Habilidades Especiales**: 12 habilidades únicas
  - 4 categorías: Ataque, Defensa, Soporte, Especial
  - Sistema de maná (100 max, +10 regeneración por turno)
  - Cooldowns individuales por habilidad
  - Desbloqueo progresivo por nivel (1-20)
  - Efectos: críticos, curación, buffs, debuffs, lifesteal
  - Clase `SkillManager` en `src/skill_system.py`
  
- **Sistema de Logros**: 20+ achievements
  - 5 categorías: Combate, Progresión, Colección, Exploración, Especial
  - Logros secretos/ocultos
  - Sistema de progreso incremental
  - Recompensas: oro y experiencia
  - Estadísticas de completitud por categoría
  - Persistencia en JSON
  - Clase `AchievementManager` en `src/achievement_system.py`
  
- **Suite de Tests Automatizados**
  - 10 tests unitarios con cobertura del 100%
  - Tests de imports, configuración, personaje, enemigos
  - Tests de sistemas nuevos (save, skills, achievements)
  - Archivo `tests/test_suite.py`
  
- **Documentación Completa**
  - `DEVELOPMENT.md`: Guía para desarrolladores
  - `CHANGELOG.md`: Historial de cambios
  - `requirements.txt`: Dependencias del proyecto
  - `setup.sh`: Script de configuración automática
  - `.gitignore`: Archivos excluidos de git
  - README.md actualizado con nuevas características

### 🔧 Cambiado
- **Refactorización Clase Enemy**
  - Renombrada de `enemy` a `Enemy` (PascalCase)
  - Implementadas `@property` para todos los atributos
  - Métodos legacy preservados para compatibilidad
  - Documentación con docstrings añadida
  
- **Refactorización Clase MainCharacter**
  - Implementadas `@property` para 10+ atributos
  - Código más pythónico y mantenible
  - Métodos legacy preservados
  - Validación automática (ej: health no puede ser negativo)
  - Integración con nuevo sistema de guardado
  
- **Sistema de Guardado**
  - `save_game()` ahora acepta parámetro `slot` (1-3)
  - `load_game()` ahora acepta parámetro `slot` (1-3)
  - Métodos legacy `save_game_legacy()` y `load_game_legacy()` disponibles

### 🐛 Corregido
- **Bug crítico en combate**: `steps_until_combat` estaba hardcodeado a 999
  - Ahora es dinámico basado en nivel del jugador (3-15 pasos)
  - Escala con dificultad: menos pasos en niveles altos
  
- **Imports duplicados**: Eliminado import duplicado de `config` en `shop.py`

- **Ruta de archivo incorrecta**: Corregida ruta de sonido en `game_menu.py`
  - De backslashes Windows (`\\`) a forward slashes (`/`)
  
- **Import incorrecto**: Actualizada importación de `enemy` a `Enemy` en `main_character.py`

### 🎯 Mejoras de Calidad
- Código más pythónico con uso de `@property`
- Type hints añadidos en código nuevo
- Docstrings completos en nuevas clases
- Manejo robusto de errores con try-except
- Separación clara de responsabilidades
- Tests automatizados para validación continua

---

## [0.3.0] - 2025-XX-XX

### 🆕 Añadido
- Sistema de configuración centralizada (`config.py`)
- Gestor de configuraciones de usuario (`settings_manager.py`)
- Sistema avanzado de gestión de pantalla (`display_manager.py`)
- Gestor de entrada mejorado (`input_manager.py`)
- Sistema de subida de nivel refactorizado

### 🔧 Cambiado
- Refactorización completa del personaje principal
- Sistema de armas mejorado con mejor manejo de errores
- Menú principal expandido con nuevas opciones
- Tienda completamente rediseñada

### 🎨 Mejoras Visuales
- Fondo de mazmorra dinámico con elementos animados
- Efectos visuales avanzados con fade in/out
- Renderizado de texto mejorado
- Nuevas fuentes tipográficas

### 📁 Restructuración
- Modularización avanzada del código
- Sistema robusto de manejo de errores
- Limpieza de archivos obsoletos
- Nueva organización de assets

### 📊 Estadísticas
- 46 archivos modificados
- 3,542 líneas agregadas
- 634 líneas eliminadas

---

## [0.2.0] - 2024-XX-XX

### 🆕 Añadido
- Sistema de combate funcional
- Enemigos con estados alterados
- Animaciones básicas en terminal
- Estructura modular inicial

### 🔧 Cambiado
- Primera implementación de sistema de progresión
- Base de datos de enemigos
- Sistema de armas básico

---

## [0.1.0] - 2024-XX-XX

### 🆕 Añadido
- Concepto inicial del proyecto
- Estructura básica de directorios
- Personaje principal básico
- Sistema de combate prototipo

---

## 🔮 Próximas Versiones

### [0.5.0] - Planificado
- [ ] Integración visual del sistema de habilidades en combate
- [ ] UI para selección de slots de guardado
- [ ] Notificaciones de logros desbloqueados
- [ ] Menú de habilidades en HUD
- [ ] Sistema de combos de habilidades
- [ ] Más habilidades para niveles 25-70

### [0.6.0] - Planificado
- [ ] Jefes únicos en niveles clave (10, 20, 30, etc.)
- [ ] Jefa final: Ella, Diosa de la Perdición (Nivel 70)
- [ ] Sistema de crafteo de objetos
- [ ] Armas legendarias con efectos especiales
- [ ] Tutorial interactivo

### [1.0.0] - Planificado
- [ ] Sistema de sprites y gráficos 2D
- [ ] Integración completa de audio
- [ ] Nuevas mazmorras y biomas
- [ ] Sistema de historia con cinemáticas
- [ ] Modo multijugador cooperativo (experimental)

---

**Formato de versiones**: `MAJOR.MINOR.PATCH`
- **MAJOR**: Cambios incompatibles en la API
- **MINOR**: Nuevas funcionalidades compatibles hacia atrás
- **PATCH**: Correcciones de bugs compatibles hacia atrás
