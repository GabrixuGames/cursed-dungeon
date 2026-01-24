# 📋 CHANGELOG

Todos los cambios notables del proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

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
