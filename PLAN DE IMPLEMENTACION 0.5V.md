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

## ⚔️ FASE 4: SISTEMA DE COMBATE POR TURNOS (Estimado: ~3 horas)

### **4.1 Refactorización Core de Combate**
**Agente: GameDevSenior**
**Archivo: `levels/dungeon_combat.py` (refactorizar)**

**Tareas:**
- [ ] Separar lógica de combate en clase `CombatManager`
- [ ] Implementar sistema de turnos basado en velocidad
- [ ] Queue de acciones (quien ataca primero)
- [ ] Pausar en turno del jugador para decisión
- [ ] Procesar acción del jugador
- [ ] Ejecutar turno del enemigo
- [ ] Actualizar cooldowns y efectos

**Pseudocódigo:**
```python
class CombatManager:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn_queue = self.calculate_turn_order()
    
    def calculate_turn_order(self):
        # Basado en velocidad/attack_rate
        pass
    
    def player_turn(self):
        # Mostrar menú, esperar decisión
        action = show_combat_menu()
        return self.process_player_action(action)
    
    def enemy_turn(self):
        # IA decide acción
        pass
```

### **4.2 Menú de Combate**
**Agente: FrontendJunior + GameDevJunior**
**Archivo: `levels/combat_menu.py` (nuevo)**

**Tareas:**
- [ ] Crear menú de 4 opciones:
  - ⚔️ **Atacar** (ataque normal)
  - ✨ **Habilidad** (submenu de skills disponibles)
  - 🎒 **Item** (submenu de items usables)
  - 🏃 **Huir** (probabilidad de escape)
- [ ] Navegación con teclado (flechas + Enter)
- [ ] Submenús para habilidades e items
- [ ] Mostrar info: maná, cooldowns, descripción
- [ ] Confirmación de acción

### **4.3 Integración Sistema de Habilidades**
**Agente: GameDevSenior**
**Archivos: `levels/dungeon_combat.py`, `src/skill_system.py`**

**Tareas:**
- [ ] Añadir `SkillManager` al MainCharacter
- [ ] Integrar habilidades en menú de combate
- [ ] Aplicar efectos de habilidades en combate
- [ ] Actualizar cooldowns cada turno
- [ ] Regenerar maná cada turno
- [ ] Mostrar feedback visual de habilidades
- [ ] Sonidos específicos por habilidad

### **4.4 Sistema de Huida**
**Agente: GameDevJunior**
**Archivo: `levels/dungeon_combat.py`**

**Tareas:**
- [ ] Calcular probabilidad de huida (basado en nivel/diferencia)
- [ ] Penalización si falla (enemigo ataca)
- [ ] Recompensa reducida si huye exitosamente
- [ ] Animación de huida
- [ ] Logro: "Cobarde" (huir 10 veces)

---

## 🎨 FASE 5: MEJORAS DE UI DE COMBATE (Estimado: ~1.8 horas)

### **⚠️ IMPORTANTE: Mantener Sistemas Existentes**

**Lo que YA existe y debemos mantener:**
- ✅ `draw_combat_scene()` con renderizado de fondo y barras HP
- ✅ `combat_message_box` (cuadro de texto persistente)
- ✅ `toast_manager` (notificaciones temporales)
- ✅ Sistema de animaciones en `src/animations/`
- ✅ Barras de vida funcionales

---

### **5.1 Reubicación de Elementos Existentes**
**Agente: FrontendSenior**
**Archivo: `levels/dungeon_combat.py` (función `draw_combat_scene`)**
**Tiempo: ~0.5 horas**

**Tareas:**
- [ ] **Reposicionar nombres**: Mover de `UI_Y = 170` a posición más alta (ej: `UI_Y = 100`)
- [ ] **Ajustar barras HP**: Seguir bajo los nombres pero con mejor spacing
- [ ] **Añadir barra de maná**: Solo para jugador, debajo de su HP
  ```python
  # Ejemplo de código a añadir:
  MP_BAR_Y = BAR_Y + 25
  player_mp = main_character.skill_manager.current_mana
  player_max_mp = main_character.skill_manager.max_mana
  mp_ratio = player_mp / player_max_mp if player_max_mp > 0 else 0
  pygame.draw.rect(screen, (50, 50, 100), (player_bar_x, MP_BAR_Y, BAR_WIDTH, BAR_HEIGHT))
  pygame.draw.rect(screen, (100, 150, 255), (player_bar_x, MP_BAR_Y, int(BAR_WIDTH * mp_ratio), BAR_HEIGHT))
  ```
- [ ] **Reposicionar `combat_message_box`**: Mover a zona inferior central
  - Actualmente se dibuja al final de `draw_combat_scene()`
  - Debe estar encima del menú de acciones (Y = screen_height - 200)

---

### **5.2 Nuevo Menú de Acciones en Combate**
**Agente: FrontendJunior**
**Archivo: `levels/combat_menu.py` (nuevo) + modificar `dungeon_combat.py`**
**Tiempo: ~0.5 horas**

**Layout objetivo:**
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
│ > Atacar  |  Habilidad  |  Item      │ ← Nuevo
│                              |  Huir  │
└──────────────────────────────────────┘
```

**Tareas:**
- [ ] Crear función `draw_combat_actions_menu(screen, font, selection, options)`
  - Se renderiza debajo del `combat_message_box`
  - En la parte inferior de la pantalla (Y = screen_height - 100)
  - 4 opciones con resaltado de selección
- [ ] Función de navegación `handle_menu_input(event, selection, max_options)`
- [ ] Integrar con el loop principal de combate

---

### **5.3 Integración con Animaciones Existentes**
**Agente: GameDevSenior**
**Archivos: `levels/dungeon_combat.py`, `src/animations/animations.py`**
**Tiempo: ~0.5 horas**

**Tareas:**
- [ ] **Mantener** todas las animaciones existentes:
  - `animation_player_atack()` ✅
  - `animation_enemy_atack()` ✅
  - `animation_player_evade()` ✅
  - `animation_enemy_evade()` ✅
  - `animation_victory()` ✅
- [ ] **Adaptar** para que funcionen con sistema de turnos:
  - Animación se ejecuta DESPUÉS de seleccionar acción
  - Pausar juego durante animación
  - Actualizar `combat_message_box` durante animación
- [ ] **Ocultar menú** durante animaciones (solo mostrar cuando es turno del jugador)

**Ejemplo de integración:**
```python
def player_attack_action(player, enemy):
    # Usuario seleccionó "Atacar"
    damage = calculate_damage(player, enemy)
    enemy.health -= damage
    
    # Ejecutar animación existente
    animation_player_atack(screen, font_text, font_ascii, player_x, player_y, 
                          inicial_player_health, hud_enemy_hp, player, enemy)
    
    # Actualizar mensaje
    combat_message_box.show(screen, font_text, f"¡Golpe! {damage} de daño")
```

---

### **5.4 Usar `combat_message_box` para Feedback**
**Agente: FrontendJunior**
**Archivo: `src/others.py` (verificar API de `combat_message_box`)**
**Tiempo: ~0.3 horas**

**Tareas:**
- [ ] Verificar métodos actuales de `combat_message_box`
- [ ] Actualizar todas las llamadas a `slow_print()` para usar `combat_message_box.show()`
- [ ] Ejemplos de mensajes:
  - "¡Golpe poderoso! 45 de daño"
  - "El Goblin te ataca por 15"
  - "Usaste Poción de Vida (+50 HP)"
  - "¡Esquivaste el ataque!"
  - "Habilidad: Segundo Aliento (+40 HP)"
  - "¡Intentas huir!"

**Ejemplo de uso:**
```python
# Antes:
slow_print(screen, font, "El enemigo te ataca", x, y)

# Después:
combat_message_box.show(screen, font, "El enemigo te ataca", timeout=1500)
```

---

## 🔗 FASE 6: INTEGRACIÓN DE SISTEMAS (Estimado: ~2 horas)

### **6.1 Sistema de Logros en Combate**
**Agente: GameDevSenior**
**Archivo: `levels/dungeon_combat.py`**

**Tareas:**
- [ ] Integrar `AchievementManager`
- [ ] Trackear eventos:
  - Enemigos derrotados
  - Esquivas consecutivas
  - Combates perfectos
  - Uso de habilidades
  - Items usados
  - Huidas exitosas
- [ ] Notificación de logro desbloqueado (usar `toast_manager`)
- [ ] Recompensa inmediata (oro/exp del logro)

### **6.2 Sistema de Guardado Actualizado**
**Agente: BackendSenior**
**Archivos: `src/object/main_character.py`, `src/save_manager.py`**

**Tareas:**
- [ ] Añadir inventario a datos de guardado
- [ ] Guardar estado de habilidades (cooldowns, maná)
- [ ] Guardar progreso de logros
- [ ] Migración de saves antiguos
- [ ] Test de integridad de guardado

### **6.3 Selector de Slots de Guardado**
**Agente: FrontendJunior**
**Archivo: `levels/save_load_menu.py` (nuevo)**

**Tareas:**
- [ ] Menú de selección de slots (3 opciones)
- [ ] Mostrar preview: nombre, nivel, fecha
- [ ] Opción de eliminar save
- [ ] Confirmación antes de sobrescribir
- [ ] Integrar en menú principal

---

## 🧪 FASE 7: TESTING Y BALANCEO (Estimado: ~1.5 horas)

### **7.1 Tests Unitarios**
**Agente: QA**
**Archivo: `tests/test_suite.py` (ampliar)**

**Tareas:**
- [ ] Test de sistema de items
- [ ] Test de inventario (add, remove, use)
- [ ] Test de combate por turnos
- [ ] Test de cálculo de turnos
- [ ] Test de huida
- [ ] Test de integración items + combate

### **7.2 Balanceo**
**Agente: GameDevSenior + QA**
**Archivos: `src/db/itemsDb.json`, `config.py`**

**Tareas:**
- [ ] Ajustar precios de items
- [ ] Balancear efectos de pociones
- [ ] Ajustar probabilidad de huida
- [ ] Balancear costos de habilidades
- [ ] Testear dificultad en diferentes niveles
- [ ] Ajustar drop rate de oro

### **7.3 Playtesting**
**Agente: QA + PM**

**Tareas:**
- [ ] Sesión de juego completa (nivel 1-15)
- [ ] Verificar fluidez del combate
- [ ] Documentar bugs encontrados
- [ ] Recopilar feedback de UX
- [ ] Verificar todos los logros

---

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
| **GameDevSenior** | Combate, habilidades, balanceo | 4h | ⏳ 0h/4h |
| **GameDevJunior** | Mecánicas secundarias, efectos | 2h | ⏳ 0h/2h |
| **BackendSenior** | Inventario, guardado, arquitectura | 2.5h | ✅ 2.5h/2.5h |
| **BackendJunior** | Items, base de datos | 2h | ✅ 2h/2h |
| **FrontendSenior** | UI mejorada, optimización | 1.5h | ✅ 1.5h/1.5h |
| **FrontendJunior** | Menús, tienda, selector saves | 2.5h | ✅ 1.5h/2.5h |
| **Designer** | UI/UX, layout, mockups | 1h | ✅ 1h/1h |
| **QA** | Testing, balanceo, bugs | 2h | ⏳ 0h/2h |
| **DocWriter** | Documentación, tutoriales | 1h | ⏳ 0h/1h |

**Progreso total: 8.5h/13.8h (~62% completado)**

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

### Completadas (3/8 fases)
- ✅ **FASE 1**: Análisis y Diseño
- ✅ **FASE 2**: Sistema de Items e Inventario
- ✅ **FASE 3**: Tienda de Items

### En Progreso
- ⏳ **FASE 4**: Sistema de Combate por Turnos (0%)
- ⏳ **FASE 5**: Mejoras de UI de Combate (0%)

### Pendientes
- ⏹️ **FASE 6**: Integración de Sistemas
- ⏹️ **FASE 7**: Testing y Balanceo
- ⏹️ **FASE 8**: Documentación

**Estado del plan: 🔄 EN PROGRESO (62% completado)**
**Última actualización: 24 de enero de 2026**
