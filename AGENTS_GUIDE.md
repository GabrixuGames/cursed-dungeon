# 🎮 GUÍA DE TRABAJO CON AGENTES

## 📋 Resumen del Sistema

Este proyecto utiliza un sistema de **agentes especializados** para organizar el desarrollo. Cada agente tiene un rol, responsabilidades y métricas específicas.

---

## 👥 Equipo de Agentes

### 🎨 Frontend Team
- **FrontendJunior** (Haiku): Implementa UI/menús en Pygame
- **FrontendSenior** (Sonnet): Optimiza rendering y performance

### 🎮 Game Development Team  
- **GameDevJunior** (Haiku): Implementa mecánicas básicas
- **GameDevSenior** (Sonnet): Arquitectura, optimización y balanceo

### ⚙️ Backend Team
- **BackendJunior** (Haiku): Sistemas de datos y lógica
- **BackendSenior** (Sonnet): Optimización y arquitectura

### 🔗 Integration
- **FullstackDev** (Sonnet): Coordinación entre sistemas

### 🎨 Design & Quality
- **Designer** (Haiku): UI/UX y game feel
- **QA** (Haiku): Testing, playtesting y balanceo

### 📊 Management
- **PM** (Sonnet 4 ⭐): Coordinación, prioridades y decisiones
- **DocWriter** (Haiku): Documentación técnica
- **DevOps** (Sonnet): Builds y deployment

---

## 🔄 Cómo Trabajar con los Agentes

### Formato de Comunicación

Cuando interactúes conmigo, **indicaré el agente activo**:

```
🎮 [GameDevJunior] - Implementando sistema de combate...
📋 [PM] - Analizando prioridades del sprint...
✅ [QA] - Testeando mecánicas de inventario...
🎨 [Designer] - Mejorando feedback visual del combate...
```

### Solicitar Trabajo de un Agente Específico

Puedes pedirme que trabaje como un agente específico:

```
"@GameDevSenior revisa el código del sistema de partículas"
"@QA testea el sistema de guardado"
"@Designer mejora el HUD de combate"
"@PM qué debería priorizar para el próximo sprint?"
```

### Flujo Típico de Trabajo

1. **PM** evalúa tu solicitud y define prioridades
2. **Agente Junior** implementa la funcionalidad base
3. **Agente Senior** revisa y optimiza
4. **QA** testea y reporta bugs
5. **DocWriter** documenta cambios

---

## 📚 Documentos Clave

### Para Empezar
- **README.md**: Overview del proyecto
- **AGENTS.md**: Definición completa de cada agente
- **WORKFLOW.md**: Procesos ágiles de desarrollo

### Estándares Técnicos
- **GAMEDEV_STANDARDS.md**: Patrones específicos de Pygame ⭐ **NUEVO**
- **STANDARS.md**: Estándares generales de código
- **DEVELOPMENT.md**: Guía técnica del proyecto

### Gestión
- **RULES.md**: Normas del equipo
- **CHANGELOG.md**: Historial de cambios
- **PLAN DE IMPLEMENTACION 0.5V.md**: Roadmap actual

---

## 🎯 Ejemplos de Uso

### Ejemplo 1: Implementar Nueva Feature

**Tú pides**:
> "Necesito añadir un sistema de críticos al combate"

**Respuesta**:
```
📋 [PM] - Evaluando feature: Sistema de críticos
Prioridad: Alta | Impacto: Mecánica core | Tiempo estimado: 2-3 días

🎮 [GameDevJunior] - Implementando sistema de críticos...
[código implementado]

🎯 [GameDevSenior] - Revisando implementación...
[optimizaciones sugeridas]

✅ [QA] - Testeando balanceo de críticos...
[reporte de bugs/feedback]

📚 [DocWriter] - Actualizando documentación...
```

### Ejemplo 2: Corregir Bug

**Tú reportas**:
> "El juego crashea al abrir el inventario con más de 10 items"

**Respuesta**:
```
✅ [QA] - Reproduciendo bug... Confirmado.
Severidad: Alta (afecta gameplay)

🎮 [GameDevJunior] - Investigando causa...
[análisis del problema]

🔧 [GameDevJunior] - Implementando fix...
[código corregido]

✅ [QA] - Validando fix... Bug resuelto ✓
```

### Ejemplo 3: Optimización

**Tú notas**:
> "El juego va a 30 FPS cuando hay muchos enemigos"

**Respuesta**:
```
📋 [PM] - Prioridad: Alta (performance crítico)

🎯 [GameDevSenior] - Analizando performance...
[profiling y diagnóstico]

🎯 [GameDevSenior] - Optimizando sistema de rendering...
- Implementando sprite groups
- Añadiendo object pooling
- Optimizando colisiones

✅ [QA] - Testeando performance...
FPS mejorado: 30 → 58 FPS ✓
```

### Ejemplo 4: Consulta de Diseño

**Tú preguntas**:
> "¿Cómo puedo mejorar el feedback visual del daño?"

**Respuesta**:
```
🎨 [Designer] - Analizando game feel...

Sugerencias:
1. Screen shake en impactos grandes
2. Números flotantes de daño (damage popups)
3. Partículas en dirección del golpe
4. Flash rojo en sprite enemigo
5. Freeze frames en críticos

🎮 [GameDevJunior] - ¿Implemento estas mejoras?
```

---

## 🚀 Comandos Rápidos

Cuando quieras trabajo específico, usa estos atajos:

### Desarrollo
- `implementa [feature]` → GameDevJunior trabaja
- `optimiza [sistema]` → GameDevSenior revisa
- `revisa [archivo]` → Senior correspondiente analiza

### Testing
- `testea [sistema]` → QA ejecuta tests
- `playtest` → QA hace sesión de playtesting
- `balancea [mecánica]` → GameDevSenior + QA iteran

### Gestión
- `prioriza` → PM evalúa y organiza tareas
- `qué sigue` → PM sugiere próximos pasos
- `estado del proyecto` → PM da reporte de avance

### Documentación
- `documenta [feature]` → DocWriter actualiza docs
- `explica [código]` → DocWriter analiza y explica

---

## 📊 Estado Actual del Proyecto

### ✅ Sistemas Implementados
- Save/Load (SaveManager)
- Sistema de habilidades (SkillManager)
- Logros (AchievementManager)
- Inventario (InventorySystem)
- Combate básico (MainCharacter, Enemy)
- Menús y navegación

### 🚧 En Desarrollo / Pendiente
- Sistema de audio completo
- Optimización de rendering
- Sistema de partículas avanzado
- Más animaciones de combate
- Balanceo de dificultad

### 📋 Backlog
- Multiplayer/Online features
- Sistema de crafting
- Más niveles/mazmorras
- Sistema de diálogos
- Tutorial interactivo

---

## 💡 Tips para Máxima Eficiencia

1. **Sé específico**: En vez de "mejora el juego", di "optimiza el rendering del combate"

2. **Usa el agente correcto**: 
   - Bugs → QA primero
   - Optimización → Seniors
   - Nuevas features → Juniors
   - Decisiones → PM

3. **Itera rápido**: No busques perfección en primera implementación

4. **Playtesting frecuente**: Pide a QA que testee regularmente

5. **Documenta decisiones**: Ayuda a DocWriter manteniendo changelog actualizado

---

## 🎮 Siguiente Paso Sugerido

**📋 [PM]** Recomendación:

Ahora que la documentación está actualizada, sugiero:

1. **Revisar el estado actual del código** con GameDevSenior
2. **Priorizar próximas features** según PLAN DE IMPLEMENTACION 0.5V.md
3. **Ejecutar suite de tests** con QA para verificar calidad actual
4. **Identificar optimizaciones críticas** para mejorar performance

**¿Qué te gustaría hacer primero?**

---

**Creado por**: PM, DocWriter  
**Fecha**: Enero 2026  
**Versión**: 1.0
