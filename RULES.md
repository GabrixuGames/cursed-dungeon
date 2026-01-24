# rules.md - Normas Generales del Equipo

## 🤝 Comunicación entre agentes
- Usa mensajes claros y concisos
- Menciona al agente específico cuando necesites su input: @PM, @GameDevSenior, etc.
- Documenta decisiones importantes en CHANGELOG.md
- Reporta blockers inmediatamente en daily standup
- Usa prefijos en mensajes:
  - `[Bug]` para reportar errores
  - `[Feature]` para proponer nuevas funcionalidades
  - `[Question]` para dudas
  - `[Review]` para solicitar revisión de código

## 💻 Estándares de código
- **Python**: snake_case para funciones/variables, PascalCase para clases
- Type hints obligatorios en funciones públicas
- Docstrings con formato Google/NumPy en todas las clases y funciones públicas
- Nombres descriptivos: `calculate_damage()` > `calc_dmg()`
- Máximo 50 líneas por función
- Comenta el "por qué", no el "qué"
- Sigue PEP 8 para Python
- Usa GAMEDEV_STANDARDS.md para patrones específicos de juegos

## 🎮 Gestión de Assets (ASCII Art Game)

### ⚠️ Filosofía Visual: Arte ASCII

Este juego utiliza **arte ASCII** para toda la representación visual:
- ✅ Personajes renderizados con caracteres
- ✅ Enemigos como arte ASCII
- ✅ UI dibujada con caracteres Unicode (│ ─ ┌ └ █ ░)
- ✅ Animaciones mediante frames ASCII
- ✅ Audio para feedback (música y SFX)

**NO se usan sprites/imágenes**:
- ❌ Sprites PNG
- ❌ Spritesheets
- ❌ Texturas bitmap

### Organización
```
src/assets/
├── fonts/              # Fuentes TTF monoespaciadas
│   ├── main.ttf       # Texto normal
│   └── ascii.ttf      # Arte ASCII (DEBE ser monoespaciada)
└── sounds/             # Audio (MP3/WAV/OGG)
    ├── combat/
    │   ├── hit.mp3
    │   ├── miss.mp3
    │   └── battle_start.mp3
    ├── ui/
    │   ├── click.mp3
    │   └── menu_select.mp3
    └── music/
        ├── main_menu.mp3
        └── ambience_sound.mp3
```

### Nomenclatura de Assets
- **Fuentes**: `font_main.ttf`, `font_ascii.ttf` (monoespaciadas)
- **Sonidos**: `sfx_category_action.mp3` (ej: `sfx_combat_hit.mp3`)
- **Música**: `music_context.mp3` (ej: `music_main_menu.mp3`)
- **Ambiente**: `ambience_dungeon.mp3`

### Arte ASCII en Código

El arte se define directamente en código Python:

```python
# Personajes como listas de strings
PLAYER_IDLE = [
    "  O  ",
    " /|\\ ",
    " / \\ "
]

ENEMY_GOBLIN = [
    " ._. ",
    "((o))",
    " /^\\ "
]

# UI con caracteres Unicode
BOX_CHARS = "┌─┐│└┘"
BLOCKS = "█▓▒░"
```

### Control de Versiones de Assets
- Fuentes: Commitear en repo (< 1MB)
- Audio: Comprimir y optimizar antes de commit
- Documentar origen en `src/assets/README.md`
- No commitear assets temporales o de prueba

## 📝 Control de versiones

### Branches
```
main          → Código estable en producción
develop       → Desarrollo activo
feature/*     → Nuevas características (ej: feature/inventory-system)
bugfix/*      → Corrección de bugs (ej: bugfix/save-corruption)
hotfix/*      → Correcciones urgentes de producción
```

### Commits
Usa **Conventional Commits**:
```
Add: Nueva característica
Fix: Corrección de bug
Refactor: Refactorización sin cambiar funcionalidad
Docs: Cambios en documentación
Test: Añadir o modificar tests
Style: Formato, espacios, etc.
Perf: Mejoras de performance
Chore: Tareas de mantenimiento

Ejemplos:
- Add: Player attack ASCII animation frames
- Fix: Resolve save file corruption on exit
- Refactor: Optimize ASCII text rendering with caching
- Docs: Update DEVELOPMENT.md with audio system
```

### Pull Requests
- Título descriptivo siguiendo convención de commits
- Descripción clara de cambios realizados
- Screenshots/GIFs para cambios visuales
- Requiere revisión de senior correspondiente antes de merge
- Tests deben pasar antes de merge

## 🎯 Prioridades

### Para Desarrollo de Juegos
1. **Diversión / Game Feel** - ¿Es divertido? ¿Se siente bien?
2. **Funcionalidad Core** - Mecánicas principales funcionando
3. **Estabilidad** - Sin crashes o bugs game-breaking
4. **Performance** - 60 FPS consistente
5. **Pulido Visual** - Animaciones, efectos, juice
6. **Features Secundarias** - Logros, estadísticas, extras

### Criterios de Decisión
- ¿Mejora la experiencia del jugador?
- ¿Impacta el timeline?
- ¿Es técnicamente viable?
- ¿Vale la pena el esfuerzo?

## 🔄 Proceso de desarrollo

### 1. Planning (PM + Seniors)
- PM define features del sprint
- Seniors evalúan viabilidad técnica
- Designer propone UX/UI
- Equipo estima esfuerzo

### 2. Implementación (Juniors)
- GameDevJunior: Mecánicas de juego
- FrontendJunior: UI y menús
- BackendJunior: Sistemas de datos
- Siguiendo GAMEDEV_STANDARDS.md

### 3. Review (Seniors)
- Code review en máximo 24h
- Feedback constructivo y educativo
- Verificación de performance
- Aprobación requerida para merge

### 4. Testing (QA)
- Tests unitarios y de integración
- Playtesting de mecánicas
- Verificación de balanceo
- Documentación de bugs

### 5. Integration (FullstackDev)
- Integrar todos los sistemas
- Resolver conflictos de dependencias
- Verificar que todo funciona junto

### 6. Polish (Designer + Seniors)
- Mejorar game feel
- Ajustar feedback visual/audio
- Pulir transiciones
- Verificar UX

### 7. Documentation (DocWriter)
- Actualizar DEVELOPMENT.md
- Documentar nuevas APIs
- Actualizar CHANGELOG.md
- Escribir guías de usuario si aplica

### 8. Deployment (DevOps)
- Crear build de release
- Testear ejecutable
- Desplegar según checklist
- Configurar monitoreo

## 🎮 Específico para Game Development

### Playtesting
- Sesiones de 30-60 minutos, 2-3 veces por semana
- Todo el equipo participa
- Documentar: bugs, feedback, ideas
- PM prioriza cambios basados en feedback

### Balanceo de Mecánicas
- GameDevSenior es responsable final
- Usar fórmulas matemáticas documentadas
- Iterar basado en playtesting
- Documentar cambios en CHANGELOG.md

### Performance Targets
- **60 FPS** mínimo en hardware objetivo
- **< 2 segundos** para carga de niveles
- **< 100 MB** de RAM usage
- **0 crashes** en sesión de 1 hora

### Quality Bar
- **0 bugs críticos** (crashes, data loss)
- **< 3 bugs altos** por release
- **80%+ cobertura** de tests en código crítico
- **Diversión verificada** por playtesting

## 📊 Métricas y Accountability

### Por Agente (ver AGENTS.md para detalles)
- **Juniors**: Entregar features en 1-2 días
- **Seniors**: Code review en < 24h
- **QA**: Reportar bugs en < 1h de descubrimiento
- **PM**: Mantener docs actualizadas
- **Designer**: Feedback positivo en playtesting

### Por Sprint
- Features completadas vs planificadas
- Bugs encontrados y resueltos
- Performance (FPS promedio)
- Satisfacción del equipo

## 🐛 Gestión de Errores

### Severidad de Bugs
1. **Crítico**: Game crashes, data corruption → Fix inmediato
2. **Alto**: Mecánicas rotas, exploits → Fix en 1-2 días
3. **Medio**: Bugs visuales, balanceo → Fix en sprint actual
4. **Bajo**: Edge cases raros, polish → Backlog

### Reporte de Bugs
```markdown
**Bug**: [Título descriptivo]
**Severidad**: Crítico/Alto/Medio/Bajo
**Reproducción**:
1. Paso 1
2. Paso 2
3. Resultado inesperado

**Esperado**: [Comportamiento correcto]
**Actual**: [Lo que sucede]
**Screenshot**: [Si aplica]
**Logs**: [Si hay errores en consola]
```

## 🚨 Situaciones de Emergencia

### Hotfix en Producción
1. PM declara emergencia
2. Se crea branch `hotfix/*`
3. Developer asignado trabaja en fix
4. Senior revisa ASAP
5. QA valida urgentemente
6. Deploy inmediato tras aprobación
7. Merge a main y develop

### Blocker Crítico
1. Reportar inmediatamente a PM
2. PM evalúa impacto en timeline
3. Equipo discute soluciones
4. PM toma decisión final
5. Ajustar plan de sprint si es necesario

## 📞 Escalación

### Conflictos Técnicos
1. Developers discuten solución
2. Si no resuelven → Senior del área
3. Si persiste → FullstackDev
4. Si afecta scope → PM

### Decisión Final
- Técnicas: FullstackDev o GameDevSenior
- Scope/Prioridades: PM
- UX/Design: Designer con veto de PM
- Emergencias: PM decide de inmediato

---

**Última actualización**: Enero 2026 - v0.5  
**Revisado por**: PM
