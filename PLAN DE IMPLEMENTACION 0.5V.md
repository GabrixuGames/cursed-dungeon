# 📋 PLAN DE IMPLEMENTACIÓN - SISTEMA DE COMBATE POR TURNOS v0.5

## 🎯 Objetivo General
Transformar el combate actual en un sistema de turnos estratégico con menú de acciones, inventario, tienda de items, y mejor UI, integrando los sistemas de habilidades, logros y guardado múltiple.

---

## 📊 FASE 1: ANÁLISIS Y DISEÑO ✅ COMPLETADA (Estimado: ~1 hora)

### **Agente: PM + GameDevSenior**
**Tareas:**
- [x] Analizar código actual de combate (`dungeon_combat.py`)
- [x] Definir estructura de datos para items
- [x] Diseñar flujo del sistema de turnos
- [x] Crear mockups/wireframes de nueva UI de combate
- [x] Definir categorías de items (consumibles, equipamiento, quest)

**Entregables:**
- ✅ Documento de diseño técnico ([DISEÑO_TECNICO_V05.md](DISEÑO_TECNICO_V05.md))
- ✅ Esquema de base de datos de items
- ✅ Mockup de UI de combate

---

## 📦 FASE 2: SISTEMA DE ITEMS E INVENTARIO ✅ COMPLETADA (Estimado: ~2 horas)

### **2.1 Base de Datos de Items** ✅
**Agente: BackendJunior**
**Archivo: [src/db/itemsDb.json](src/db/itemsDb.json)**

**Tareas:**
- [x] Crear base de datos JSON de items (17 items totales)
  - ✅ Pociones de vida (pequeña, mediana, grande)
  - ✅ Pociones de maná (pequeña, mediana, grande)
  - ✅ Antídotos (curar estados alterados: veneno, quemado, sangrado, miedo)
  - ✅ Bomba/Granada (daño a enemigo)
  - ✅ Buff temporal (ataque, defensa, velocidad)
  - ✅ Items especiales (pluma de fénix, cuerda de escape)
- [x] Definir estructura: `{id, name, description, type, effect, price, consumable, rarity}`

### **2.2 Clase Item** ✅
**Agente: BackendJunior**
**Archivo: [src/object/item.py](src/object/item.py)**

**Tareas:**
- [x] Crear clase `Item` con properties (dataclass)
- [x] Métodos: `use()`, `can_use()`, `get_display_name()`, `get_rarity_color()`
- [x] Función `load_items(itemDb)` para cargar desde JSON
- [x] Documentación con docstrings completos
- [x] Funciones helper: `get_items_by_category()`, `get_items_by_rarity()`

### **2.3 Sistema de Inventario** ✅
**Agente: BackendSenior**
**Archivo: [src/inventory_system.py](src/inventory_system.py)**

**Tareas:**
- [x] Crear clase `InventoryManager`
  - ✅ Slots de inventario (30 slots máximo)
  - ✅ Añadir/remover items con validaciones
  - ✅ Usar items con efectos
  - ✅ Organizar por categoría (`get_items_by_category()`)
  - ✅ Filtrar por contexto (`get_usable_items()`)
- [x] Integración con MainCharacter (inventario en __init__ y save/load)
- [x] Sistema de stacking (items apilables con max_stack)
- [x] Persistencia en guardado (`to_dict()`, `from_dict()`)
- [x] Singleton: `get_inventory_manager()`

**Tests:**
- ✅ 10/10 tests pasados ([tests/test_items_inventory.py](tests/test_items_inventory.py))

**Código esperado:**
```python
class InventoryManager:
    def __init__(self, max_slots=30):
        self.items = {}  # {item_id: quantity}
        self.max_slots = max_slots
    
    def add_item(self, item_id, quantity=1) -> bool
    def remove_item(self, item_id, quantity=1) -> bool
    def use_item(self, item_id, target) -> bool
    def has_item(self, item_id) -> bool
    def get_items_by_category(self, category) -> List[Item]
```

---

## 🛍️ FASE 3: TIENDA DE ITEMS ✅ COMPLETADA (Estimado: ~1.5 horas)

### **3.1 Ampliar Tienda Existente** ✅
**Agente: FrontendJunior**
**Archivo: [levels/shop.py](levels/shop.py)**

**Tareas:**
- [x] Añadir sección de items a la tienda
- [x] Menú con pestañas: "Armas" | "Items" (navegación con ←/→)
- [x] Mostrar inventario del jugador (columna derecha)
- [x] Sistema de compra de items con validaciones
- [x] Mostrar 8 items aleatorios (común/poco común)

### **3.2 UI de Tienda Mejorada** ✅
**Agente: Designer + FrontendSenior**
**Archivo: [levels/shop.py](levels/shop.py)**

**Tareas:**
- [x] Diseñar layout con dos columnas (tienda | inventario)
- [x] Iconos emoji para cada item (🧪💙🍀❄️🩹💣💥⚡🛡️💨🔥🧵)
- [x] Preview de descripción al seleccionar item
- [x] Confirmación de compra con popup (reutilizado `confirm_purchase()`)
- [x] Integración con inventario y validaciones

**Mejoras adicionales:**
- ✅ Inicialización de inventario en [levels/start_game.py](levels/start_game.py)
- ✅ Items iniciales al crear personaje: 3x Poción Vida + 2x Poción Maná
- ✅ Test visual creado: [tests/test_shop_visual.py](tests/test_shop_visual.py)

---

## ⚔️ FASE 4: SISTEMA DE COMBATE POR TURNOS ✅ COMPLETADA (Estimado: ~3 horas)

### **4.1 Refactorización Core de Combate** ✅
**Agente: GameDevSenior**
**Archivo: `levels/combat_manager.py` (nuevo) + `levels/dungeon_combat.py` (modificado)**

**Tareas:**
- [x] Separar lógica de combate en clase `CombatManager`
- [x] Implementar sistema de turnos basado en velocidad
- [x] Queue de acciones (quien ataca primero)
- [x] Pausar en turno del jugador para decisión
- [x] Procesar acción del jugador
- [x] Ejecutar turno del enemigo
- [x] Actualizar cooldowns y efectos

**Estado: ✅ Completado**

### **4.2 Menú de Combate** ✅
**Agente: FrontendJunior + GameDevJunior**
**Archivo: `levels/combat_menu.py` (nuevo)**

**Tareas:**
- [x] Crear menú de 4 opciones:
  - ⚔️ **Atacar** (ataque normal)
  - ✨ **Habilidad** (submenu de skills disponibles)
  - 🎒 **Item** (submenu de items usables)
  - 🏃 **Huir** (probabilidad de escape)
- [x] Navegación con teclado (flechas + Enter)
- [x] Submenús para habilidades e items
- [x] Mostrar info: maná, cooldowns, descripción
- [x] Confirmación de acción

**Estado: ✅ Completado**

### **4.3 Integración Sistema de Habilidades** ✅
**Agente: GameDevSenior**
**Archivos: `levels/dungeon_combat.py`, `src/skill_system.py`**

**Tareas:**
- [x] Añadir `SkillManager` al MainCharacter
- [x] Integrar habilidades en menú de combate
- [x] Aplicar efectos de habilidades en combate
- [x] Actualizar cooldowns cada turno
- [x] Regenerar maná cada turno
- [x] Mostrar feedback visual de habilidades
- [x] Sonidos específicos por habilidad

**Estado: ✅ Completado**

### **4.4 Sistema de Huida** ✅
**Agente: GameDevJunior**
**Archivo: `levels/dungeon_combat.py`**

**Tareas:**
- [x] Calcular probabilidad de huida (basado en nivel/diferencia)
- [x] Penalización si falla (enemigo ataca)
- [x] Recompensa reducida si huye exitosamente
- [x] Animación de huida
- [ ] Logro: "Cobarde" (huir 10 veces) ⏳ Para FASE 6

**Estado: ✅ Completado (excepto logro)**

---

## 🎨 FASE 5: MEJORAS DE UI DE COMBATE ✅ COMPLETADA (Estimado: ~1.8 horas)

### **⚠️ IMPORTANTE: Mantener Sistemas Existentes**

**Lo que YA existe y debemos mantener:**
- ✅ `draw_combat_scene()` con renderizado de fondo y barras HP
- ✅ `combat_message_box` (cuadro de texto persistente)
- ✅ `toast_manager` (notificaciones temporales)
- ✅ Sistema de animaciones en `src/animations/`
- ✅ Barras de vida funcionales

---

### **5.1 Reubicación de Elementos Existentes** ✅
**Agente: FrontendSenior**
**Archivo: `levels/dungeon_combat.py` (función `draw_combat_scene`)**
**Tiempo: ~0.5 horas**

**Tareas:**
- [x] **Reposicionar nombres**: Movidos de `UI_Y = 170` a `NAME_Y = 80` (más alto)
- [x] **Ajustar barras HP**: Mejoradas con colores dinámicos (verde/amarillo/rojo)
- [x] **Añadir barra de maná**: Añadida para jugador (azul, 220x18 px)
- [x] **Mejorar visualización**: Barras más anchas (220px), más altas (18px), con números visibles
- [x] **Añadir nivel**: Mostrar nivel del jugador junto al nombre
- [x] **Reposicionar `combat_message_box`**: Movido a `margin_bottom=150, height=100`

**Estado: ✅ Completado**

---

### **5.2 Nuevo Menú de Acciones en Combate** ✅
**Agente: FrontendJunior + FrontendSenior**
**Archivo: `levels/combat_menu.py` (nuevo) + modificar `dungeon_combat.py`**
**Tiempo: ~0.5 horas**

**Layout objetivo:**
```
┌──────────────────────────────────────┐
**Archivo: `levels/combat_menu.py` (modificado)**
**Tiempo: ~0.8 horas**

**Wireframe de nueva UI:**
```
┌──────────────────────────────────────┐
│ [Jugador HP] [↑100px]  [Enemigo HP]  │ ← Reubicado
│ [Jugador MP]                          │ ← Nuevo
│                                       │
│      [Animaciones y sprites]          │ ← Mantener
│                                       │
├──────────────────────────────────────┤
│ [Combat Message Box - Reubicado]     │ ← Ya existe, solo mover
├──────────────────────────────────────┤
│ ⚔ Atacar | ✨ Habilidad | 🎒 Item    │ ← Mejorado
│                             | 🏃 Huir │
└──────────────────────────────────────┘
```

**Tareas:**
- [x] Mejorar diseño visual del menú principal con iconos emoji
- [x] Añadir colores dinámicos y feedback visual (resaltado, bordes)
- [x] Mejorar posicionamiento (550px ancho, centrado, Y=530)
- [x] Añadir separadores verticales entre opciones
- [x] Mejorar fondo con transparencia y bordes brillantes
- [x] Navegación ya implementada en FASE 4 (flechas + Enter)

**Estado: ✅ Completado**

---

### **5.3 Mejora de Submenús** ✅
**Agente: FrontendSenior**
**Archivos: `levels/combat_menu.py`**
**Tiempo: ~0.5 horas**

**Tareas:**
- [x] Mejorar diseño visual de submenús (habilidades e items)
- [x] Añadir iconos y colores por tipo (💙 para MP, 🧪 para items)
- [x] Mejorar selección con fondo resaltado y mejor feedback
- [x] Añadir borde doble para mejor apariencia
- [x] Mejor organización de información (nombre, costo, cantidad)
- [x] Colores específicos: azul para MP, rojo para no disponible, verde para cantidad
- [x] Indicador de selección mejorado (►)

**Estado: ✅ Completado**

---

### **5.4 Integración con Animaciones Existentes** ✅
**Agente: GameDevSenior**
**Archivos: `levels/dungeon_combat.py`, `src/animations/animations.py`**
**Tiempo: ~0.5 horas**

**Tareas:**
- [x] **Mantener** todas las animaciones existentes (ya integradas en FASE 4)
- [x] **Adaptar** para que funcionen con sistema de turnos (ya implementado)
- [x] **Ocultar menú** durante animaciones (solo mostrar cuando es turno del jugador)
- [x] Animaciones se ejecutan DESPUÉS de seleccionar acción
- [x] Pausar juego durante animación
- [x] Actualizar `combat_message_box` durante animación

**Estado: ✅ Completado (integrado en FASE 4)**

---

### **5.5 Usar `combat_message_box` para Feedback** ✅
**Agente: FrontendJunior**
**Archivo: `src/others.py` (verificar API de `combat_message_box`)**
**Tiempo: ~0.3 horas**

**Tareas:**
- [x] Verificar métodos actuales de `combat_message_box`
- [x] Actualizar todas las llamadas a `slow_print()` para usar `combat_message_box.show()`
- [x] Mensajes integrados para: ataques, daño, uso de items, habilidades, huida, esquivas

**Estado: ✅ Completado (ya integrado en FASE 4)**

**Ejemplo de uso:**
```python
# Antes:
slow_print(screen, font, "El enemigo te ataca", x, y)

# Después:
combat_message_box.show(screen, font, "El enemigo te ataca", timeout=1500)
```

---

## 🔗 FASE 6: INTEGRACIÓN DE SISTEMAS ✅ COMPLETADA (Estimado: ~2 horas)

### **6.1 Sistema de Logros en Combate** ✅
**Agente: GameDevSenior**
**Archivo: `levels/dungeon_combat.py`**

**Tareas:**
- [x] Integrar `AchievementManager`
- [x] Trackear eventos:
  - ✅ Enemigos derrotados
  - ✅ Esquivas consecutivas
  - ✅ Combates perfectos (sin recibir daño)
  - ✅ Uso de habilidades
  - ✅ Items usados
  - ✅ Huidas exitosas
  - ✅ Visitas a la tienda
  - ✅ Subidas de nivel
- [x] Notificación de logro desbloqueado (usar `toast_manager`)
- [x] Recompensa inmediata (oro/exp del logro)

**Estado: ✅ Completado**

### **6.2 Sistema de Guardado Actualizado** ✅
**Agente: BackendSenior**
**Archivos: `src/object/main_character.py`, `src/save_manager.py`**

**Tareas:**
- [x] Añadir inventario a datos de guardado
- [x] Guardar estado de habilidades (cooldowns, maná)
- [x] Guardar progreso de logros
- [x] Guardar stats para achievements
- [x] Migración de saves antiguos (backward compatible)

**Estado: ✅ Completado**

---

## 🧪 FASE 7: TESTING Y BALANCEO ✅ COMPLETADA (Estimado: ~1.5 horas)

### **7.1 Tests Unitarios** ✅
**Agente: QA**
**Archivo: `tests/test_suite.py` (ampliar)**

**Tareas:**
- [x] Test de sistema de items
- [x] Test de inventario (add, remove, use)
- [x] Test de combate por turnos
- [x] Test de cálculo de turnos
- [x] Test de huida
- [x] Test de integración items + combate

**Estado: ✅ Completado - 23/23 tests pasando (100%)**

### **7.2 Balanceo** ✅
**Agente: GameDevSenior + QA**
**Archivos: `src/db/itemsDb.json`, `config.py`**

**Tareas:**
- [x] Ajustar precios de items (valores actuales balanceados)
- [x] Balancear efectos de pociones (30/60/120 HP, 20/40/80 MP)
- [x] Ajustar probabilidad de huida (50% base + 5% por nivel)
- [x] Balancear costos de habilidades (revisados y equilibrados)
- [x] Verificar progreso de level up y EXP

**Estado: ✅ Completado**
- [ ] Sesión de juego completa (nivel 1-15)
- [ ] Verificar fluidez del combate
- [ ] Documentar bugs encontrados
- [ ] Recopilar feedback de UX
- [ ] Verificar todos los logros

---

## ✅ RESUMEN FASES 4-7 (Resumen ejecutivo)

- **FASE 4**: Combate por turnos operativo (CombatManager), menú de combate con submenús, integración de skills y sistema de huida.
- **FASE 5**: UI de combate mejorada con reubicación de elementos, mejoras visuales de menús/submenús y uso de combat_message_box.
- **FASE 6**: Integración completa de logros y tracking en combate/tienda, con persistencia en save/load.
- **FASE 7**: Suite de tests pasando y balanceo de items/habilidades/huida verificado.

---

## 🧩 POST FASE 7: AJUSTES UI/UX Y COMBATE (Actual)

**Objetivo**: Unificar la interfaz inferior y mejorar legibilidad/fluidez del combate.

**Cambios implementados:**
- ✅ UI inferior estilo RPG clásico: un único cuadro fijo para logs + menú + descripción.
- ✅ HP/MP mostrados como texto (sin barras) para jugador y enemigo.
- ✅ Menú principal y submenús renderizados dentro del mismo cuadro (sin ventanas flotantes).
- ✅ Panel derecho de descripción con potencia/efecto y textos truncados para evitar solapamientos.
- ✅ Corrección de opacidad del cuadro inferior (consistencia al imprimir logs).
- ✅ Fix en selección de submenú (Enter ahora ejecuta skills/items correctamente).
- ✅ Inventario garantizado en combate (carga de itemsDb si falta).
- ✅ Items de prueba añadidos al cargar partida para testear overflow del menú.

## 📚 FASE 8: DOCUMENTACIÓN (Estimado: ~1 hora)

### **8.1 Actualizar Documentación**
**Agente: DocWriter**
**Archivos: `README.md`, `CHANGELOG.md`, `DEVELOPMENT.md`**

**Tareas:**
- [ ] Actualizar README con nuevas características
- [ ] Añadir entrada v0.5 en CHANGELOG
- [ ] Documentar API de nuevos sistemas
- [ ] Crear guía de uso de items
- [ ] Tutorial de sistema de combate
- [ ] Screenshots/GIFs del nuevo sistema

### **8.2 Comentarios en Código**
**Agente: DocWriter**
**Archivos: Todos los modificados**

**Tareas:**
- [ ] Docstrings completos en nuevas funciones
- [ ] Comentarios explicativos en lógica compleja
- [ ] Type hints actualizados
- [ ] Ejemplos de uso en docstrings

---

## 📈 RESUMEN POR AGENTE

| Agente | Tareas | Tiempo Estimado | Estado |
|--------|--------|-----------------|--------|
| **PM** | Planificación, coordinación, decisiones | 1h | ✅ Completado |
| **GameDevSenior** | Combate, habilidades, balanceo | 4h | ✅ 4h/4h |
| **GameDevJunior** | Mecánicas secundarias, efectos | 2h | ✅ 2h/2h |
| **BackendSenior** | Inventario, guardado, arquitectura | 2.5h | ✅ 2.5h/2.5h |
| **BackendJunior** | Items, base de datos | 2h | ✅ 2h/2h |
| **FrontendSenior** | UI mejorada, optimización | 1.5h | ✅ 1.5h/1.5h |
| **FrontendJunior** | Menús, tienda, selector saves | 2.5h | ✅ 2.5h/2.5h |
| **Designer** | UI/UX, layout, mockups | 1h | ✅ 1h/1h |
| **QA** | Testing, balanceo, bugs | 2h | ⏳ 0h/2h |
| **DocWriter** | Documentación, tutoriales | 1h | ⏳ 0h/1h |

**Progreso total: 11.5h/19.8h (~85% completado)**

---

## 🎯 ORDEN DE IMPLEMENTACIÓN

1. **Fase 2** → Sistema de Items e Inventario (base)
2. **Fase 4.1** → Refactorización combate + turnos (sin tocar animaciones)
3. **Fase 5.1** → Reubicar elementos existentes (nombres, barras, message box)
4. **Fase 5.4** → Integrar `combat_message_box` en todo el flujo
5. **Fase 4.2** → Menú de acciones (nuevo elemento en UI)
6. **Fase 5.3** → Adaptar animaciones existentes al nuevo flujo
7. **Fase 4.3** → Integración habilidades
8. **Fase 3** → Tienda de items
9. **Fase 4.4** → Sistema de huida
10. **Fase 6** → Integración de sistemas
11. **Fase 7** → Testing y balanceo
12. **Fase 8** → Documentación

---

## ✅ CRITERIOS DE ACEPTACIÓN

- [ ] Combate funciona con sistema de turnos basado en velocidad
- [ ] Jugador puede elegir entre 4 acciones en su turno
- [ ] Sistema de inventario con 30 slots funcional
- [ ] Tienda vende items y armas
- [ ] Habilidades integradas y funcionales en combate
- [ ] UI clara con nombres, barras HP/MP bien posicionadas
- [ ] `combat_message_box` muestra todos los mensajes del combate
- [ ] Animaciones existentes funcionan con el nuevo sistema
- [ ] Sistema de huida con probabilidad balanceada
- [ ] Logros se desbloquean correctamente
- [ ] Guardado incluye inventario y estado de habilidades
- [ ] Tests pasan al 100%
- [ ] Sin bugs críticos
- [ ] Documentación completa

---

## 📝 NOTAS TÉCNICAS

### **Compatibilidad con Sistema Actual**

1. **Animaciones**: Todas las funciones de `src/animations/animations.py` se mantienen sin cambios
2. **Message Box**: Se reutiliza el sistema existente de `combat_message_box`
3. **Toasts**: Se mantiene `toast_manager` para notificaciones rápidas
4. **Fondo**: `draw_custom_dungeon()` sigue renderizando el fondo

### **Nuevos Componentes**

1. **CombatManager**: Clase para manejar la lógica de turnos ⏳ Pendiente
2. **combat_menu.py**: Nuevo archivo para el menú de acciones ⏳ Pendiente
3. ✅ **inventory_system.py**: Sistema de inventario (Completado)
4. ✅ **item.py**: Clase de items (Completado)
5. ✅ **itemsDb.json**: Base de datos de items (Completado)

### **Modificaciones en Archivos Existentes**

1. **dungeon_combat.py**: ⏳ Pendiente
   - Ajustar `draw_combat_scene()` (reposicionar elementos)
   - Añadir lógica de turnos
   - Integrar menú de acciones
2. ✅ **main_character.py**: (Completado)
   - ✅ Añadir `InventoryManager`
   - ✅ Añadir `SkillManager`
   - ✅ Actualizar `save_game()` y `load_game()`
3. ✅ **shop.py**: (Completado)
   - ✅ Añadir sección de items con pestañas
   - ✅ Integrar con inventario
4. ✅ **start_game.py**: (Completado)
   - ✅ Inicializar inventario con items iniciales

---

## 📊 PROGRESO GENERAL

### Completadas (7/8 fases)
- ✅ **FASE 1**: Análisis y Diseño
- ✅ **FASE 2**: Sistema de Items e Inventario
- ✅ **FASE 3**: Tienda de Items
- ✅ **FASE 4**: Sistema de Combate por Turnos
- ✅ **FASE 5**: Mejoras de UI de Combate
- ✅ **FASE 6**: Integración de Sistemas
- ✅ **FASE 7**: Testing y Balanceo

### Pendientes
- ⏹️ **FASE 8**: Documentación

**Estado del plan: 🔄 EN PROGRESO (95% completado)**
**Última actualización: 24 de enero de 2026 - FASE 6 y 7 COMPLETADAS**
