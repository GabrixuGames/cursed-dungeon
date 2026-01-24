# workflow.md - Flujo de Trabajo del Equipo

## 🎮 Desarrollo Ágil para Videojuegos

### Filosofía de Desarrollo
- **Iteración rápida**: Prototipar, probar, iterar
- **Priorizar diversión**: Si no es divertido, no sirve
- **Feedback constante**: Playtesting frecuente
- **Documentar decisiones**: Mantener histórico de cambios

---

## 📅 Ciclo de Desarrollo (Sprints de 1-2 semanas)

### 1. Sprint Planning
**Participantes**: PM, GameDevSenior, Designer  
**Duración**: 1-2 horas

1. **PM** define objetivos del sprint
2. **GameDevSenior** evalúa viabilidad técnica
3. **Designer** propone mejoras de UX/feel
4. Equipo selecciona features a implementar
5. Se asignan tareas según especialidad

**Output**: Lista priorizada de tareas en plan de sprint

---

### 2. Desarrollo Iterativo

#### Día 1-2: Implementación Core
- **GameDevJunior**: Implementa mecánicas básicas
- **FrontendJunior**: Crea UI necesaria
- **BackendJunior**: Configura sistemas de datos
- **Daily standup**: 15 min al inicio del día

#### Día 3-4: Integración y Pulido
- **FullstackDev**: Integra todos los sistemas
- **GameDevSenior**: Revisa y optimiza código
- **FrontendSenior**: Mejora rendering y animaciones
- **Designer**: Ajusta feedback visual

#### Día 5-6: Testing y Balanceo
- **QA**: Ejecuta tests y playtesting
- **QA**: Documenta bugs encontrados
- **GameDevSenior**: Balancea mecánicas según feedback
- Desarrolladores corrigen bugs críticos

#### Día 7: Review y Retrospectiva
- **PM**: Sprint review con demos
- Equipo evalúa: ¿Es divertido? ¿Funciona bien?
- Retrospectiva: ¿Qué mejorar?
- **DocWriter**: Actualiza documentación

---

## 🔄 Flujo de Trabajo por Feature

### Implementación de Nueva Mecánica

```
1. PM define requisitos
   ↓
2. Designer propone feedback visual/audio
   ↓
3. GameDevSenior diseña arquitectura
   ↓
4. GameDevJunior implementa código base
   ↓
5. FrontendJunior añade UI necesaria
   ↓
6. FullstackDev integra sistemas
   ↓
7. QA testea y reporta bugs
   ↓
8. GameDevSenior revisa y optimiza
   ↓
9. Designer ajusta game feel
   ↓
10. QA valida fixes
    ↓
11. PM aprueba feature
    ↓
12. DocWriter documenta
```

### Corrección de Bug

```
1. QA descubre y documenta bug
   ↓
2. PM prioriza (crítico/alto/medio/bajo)
   ↓
3. Developer correspondiente investiga
   ↓
4. Developer implementa fix
   ↓
5. QA valida que bug está resuelto
   ↓
6. Senior revisa si es cambio mayor
```

---

## 🎯 Prioridades de Desarrollo

### Orden de Importancia

1. **Diversión / Game Feel**
   - ¿Es satisfactorio jugar?
   - ¿Hay feedback visual/audio inmediato?
   - ¿Se siente responsive?

2. **Funcionalidad Core**
   - Mecánicas principales funcionan
   - Sin crashes o game-breaking bugs
   - Save/Load funciona correctamente

3. **Performance**
   - 60 FPS consistente
   - Tiempos de carga aceptables
   - Sin memory leaks

4. **Pulido Visual**
   - Animaciones suaves
   - Efectos de partículas
   - Transiciones fluidas

5. **Features Secundarias**
   - Logros y achievements
   - Estadísticas detalladas
   - Opciones avanzadas

---

## 📋 Dailyalización

### Daily Standup (10-15 minutos)
**Hora**: Inicio del día de trabajo  
**Formato**: Cada agente responde:

1. **¿Qué hice ayer?**
2. **¿Qué haré hoy?**
3. **¿Tengo algún blocker?**

**PM** anota blockers y coordina soluciones

### Playtesting Sessions (30-60 minutos, 2-3 veces por semana)
**Participantes**: Todo el equipo

1. Jugar la build actual
2. Anotar: bugs, feedback, ideas
3. Discutir: ¿Qué funciona? ¿Qué no?
4. **PM** prioriza cambios basados en feedback

### Code Review (continuo)
- Seniors revisan código de juniors en máximo 24h
- Feedback constructivo y educativo
- Aprobación requerida antes de merge

---

## 🔧 Gestión de Cambios

### Cambios Menores (< 1 hora de trabajo)
- Aprobación del **Senior** del área
- Implementar directamente
- Actualizar documentación si aplica

### Cambios Medianos (1-4 horas)
- Discusión con **FullstackDev**
- Evaluación de impacto en otros sistemas
- Aprobación de **PM** si afecta scope

### Cambios Mayores (> 4 horas)
- Reunión con **PM** y **Seniors**
- Evaluación de:
  - Impacto en timeline
  - Recursos necesarios
  - Beneficio vs costo
- **PM** toma decisión final

### Cambios de Arquitectura
- Reunión de equipo completo
- **GameDevSenior** presenta propuesta
- Evaluación de pros/cons
- Votación si es necesario
- **PM** tiene veto en caso de empate

---

## 🐛 Gestión de Bugs

### Severidad

**Crítico** (Fix inmediato)
- Game crashes
- Data corruption
- Unplayable states

**Alto** (Fix en 1-2 días)
- Mecánicas no funcionan correctamente
- Exploits importantes
- Performance severa (< 30 FPS)

**Medio** (Fix en sprint actual)
- Bugs visuales molestos
- Balanceo incorrecto
- UX confusa

**Bajo** (Backlog)
- Bugs estéticos menores
- Edge cases raros
- Nice-to-have features

### Proceso

1. **QA** crea reporte detallado
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots/logs si aplica

2. **PM** asigna severidad y developer

3. Developer investiga y corrige

4. **QA** valida fix

5. **PM** cierra ticket

---

## 🚀 Release Checklist

### Pre-Release (1 semana antes)

- [ ] **QA**: Todos los tests pasan
- [ ] **QA**: Playtesting completo sin bugs críticos
- [ ] **GameDevSenior**: Performance aceptable (60 FPS)
- [ ] **PM**: Features planificadas completadas
- [ ] **DocWriter**: Documentación actualizada
- [ ] **DevOps**: Build de release creado y testeado

### Release Day

- [ ] **PM**: Aprobación final
- [ ] **DevOps**: Deploy a producción
- [ ] **DocWriter**: Actualizar CHANGELOG.md
- [ ] **PM**: Comunicar release
- [ ] Equipo monitorea feedback inicial

### Post-Release (1 semana después)

- [ ] **QA**: Monitorear reportes de usuarios
- [ ] **PM**: Analizar feedback
- [ ] **GameDevSenior**: Revisar métricas de performance
- [ ] Equipo planifica hotfixes si es necesario
- [ ] Retrospectiva de release

---

## 🤝 Colaboración entre Agentes

### Interacciones Comunes

**PM ↔️ Todos**
- Define prioridades
- Resuelve conflictos
- Aprueba cambios mayores

**GameDevSenior ↔️ GameDevJunior**
- Code review
- Mentorship técnico
- Arquitectura de sistemas

**FrontendSenior ↔️ FrontendJunior**
- Optimización de rendering
- Implementación de animaciones
- UI/UX best practices

**FullstackDev ↔️ Todos**
- Integración de sistemas
- Resolución de dependencias
- Coordinación técnica

**Designer ↔️ Developers**
- Especificación de UI/UX
- Feedback de implementación
- Iteración de game feel

**QA ↔️ Developers**
- Reporte de bugs
- Validación de fixes
- Sugerencia de tests

**DocWriter ↔️ Todos**
- Documentación de features
- Actualización de guías
- Clarificación de procesos

---

## 📞 Resolución de Conflictos

### Nivel 1: Entre Desarrolladores
- Discusión técnica directa
- Buscar consenso mediante código
- Si no se resuelve → Escalar

### Nivel 2: Senior del Área
- **FrontendSenior** para temas de UI
- **GameDevSenior** para mecánicas
- **BackendSenior** para datos/APIs
- Si no se resuelve → Escalar

### Nivel 3: FullstackDev
- Evalúa impacto en sistema completo
- Propone solución técnica
- Si afecta scope → Escalar

### Nivel 4: PM
- Toma decisión basada en:
  - Impacto en timeline
  - Beneficio para el juego
  - Recursos disponibles
- Decisión es final

---

## 📊 Métricas de Éxito

### Por Sprint
- Features completadas vs planificadas
- Bugs encontrados y resueltos
- Cobertura de tests
- Satisfacción del equipo (encuesta)

### Por Release
- Performance (FPS promedio)
- Crash rate
- User feedback (si aplicable)
- Tiempo de desarrollo vs estimado

### A Largo Plazo
- Velocidad del equipo (story points/sprint)
- Calidad del código (deuda técnica)
- Moral del equipo
- Cumplimiento de roadmap

---

**Última actualización**: Enero 2026 - v0.5  
**Revisado por**: PM
