# 📐 DOCUMENTO DE DISEÑO TÉCNICO - v0.5
## Sistema de Combate por Turnos, Items e Inventario

**Fecha:** 24 de enero de 2026  
**Versión:** 0.5  
**Agentes responsables:** PM + GameDevSenior

---

## 1. 🎯 RESUMEN EJECUTIVO

### Objetivos
Transformar el sistema de combate actual (tiempo real basado en velocidad) a un sistema de **combate por turnos estratégico** con las siguientes características:

1. **Menú de acciones en combate**: Atacar, Habilidad, Item, Huir
2. **Sistema de inventario**: 30 slots para gestionar items consumibles y equipables
3. **Base de datos de items**: Pociones, consumibles de combate, buffs temporales
4. **Tienda ampliada**: Venta de armas + items
5. **UI mejorada**: Reposicionamiento de elementos, barra de maná, menú de acciones
6. **Integración completa**: Skills, logros, guardado múltiple

### Alcance
- **Incluido**: Sistema de turnos, items, inventario, tienda, UI, integración de sistemas existentes
- **Excluido**: Jefes finales, combate PvP, modo multijugador

---

## 2. 📊 ANÁLISIS DEL CÓDIGO ACTUAL

### 2.1 Arquitectura Actual del Combate

**Archivo principal:** `levels/dungeon_combat.py`

#### Funciones principales:
```python
def dungeon(main_character, screen, font_ascii, font_text_combat)
    ├── dungeon_walking()  # Exploración de mazmorra
    ├── run_combat()       # Loop principal de combate
    └── draw_combat_scene() # Renderizado de UI

def run_combat(main_character, screen, ..., enemy_instance)
    ├── Combate basado en tiempos (attack_speed)
    ├── Cálculo de evasión (random chance)
    ├── Aplicación de estados alterados
    ├── Detección de victoria/derrota
    └── Retorna: ("victory"/"defeat", offset, char_offset)
```

#### Características clave identificadas:
- ✅ **Sistema de animaciones** funcional en `src/animations/animations.py`
- ✅ **combat_message_box** implementado para mensajes persistentes
- ✅ **toast_manager** para notificaciones temporales
- ✅ **Barras de HP** con diseño simétrico (jugador izquierda, enemigo derecha)
- ✅ **Sistema de estados alterados** (veneno, quemado, sangrado, miedo)
- ⚠️ **Combate en tiempo real**: Los ataques se ejecutan automáticamente según `attack_rate`
- ⚠️ **Sin menú de decisión**: El jugador no elige acciones

### 2.2 Estructura de Datos Actual

#### MainCharacter (src/object/main_character.py)
```python
class MainCharacter:
    _name: str
    _level: int
    _damage: int
    _health: int
    _evade_chance: float
    _experience: float
    _weapon: dict
    _money: int
    _atributes: int
    _to_next_level: float
    _state: dict | None
```

#### Enemy (src/object/enemy.py)
```python
class Enemy:
    _name: str
    _health: int
    _damage: int
    _attack_rate: float
    _evade_chance: float
    _level_min: int
    _level_max: int
    _exp: float
    _gold: int
    _state: list[dict]  # Estados que puede aplicar
```

#### Weapon (weaponsDb.json)
```json
{
    "name": "Espada Recta",
    "damage": 7,
    "attack_ratio": 0.7,
    "price": 75
}
```

#### Enemy States (enemyDb.json)
```json
"states": [
    {
        "state": "Envenenado",
        "chance": 30,
        "duration": 3,
        "effect": {"health": -4}
    }
]
```

### 2.3 Sistemas Existentes a Integrar

| Sistema | Archivo | Estado | Integración |
|---------|---------|--------|-------------|
| **SaveManager** | `src/save_manager.py` | ✅ Implementado | Guardar inventario y cooldowns |
| **SkillManager** | `src/skill_system.py` | ✅ Implementado | Integrar en menú de habilidades |
| **AchievementManager** | `src/achievement_system.py` | ✅ Implementado | Trackear uso de items |
| **Animaciones** | `src/animations/animations.py` | ✅ Funcional | Adaptar a sistema de turnos |
| **combat_message_box** | `src/others.py` | ✅ Funcional | Usar para todo feedback |

---

## 3. 🎨 DISEÑO DE NUEVO SISTEMA

### 3.1 Sistema de Items

#### 3.1.1 Esquema de Base de Datos (itemsDb.json)

```json
{
    "consumables": [
        {
            "id": "hp_potion_small",
            "name": "Poción de Vida Pequeña",
            "description": "Restaura 30 puntos de vida",
            "type": "consumable",
            "category": "healing",
            "effect": {
                "health": 30
            },
            "target": "self",
            "usable_in": ["combat", "dungeon"],
            "price": 25,
            "rarity": "common",
            "stackable": true,
            "max_stack": 10,
            "icon": "🧪"
        },
        {
            "id": "hp_potion_medium",
            "name": "Poción de Vida Mediana",
            "description": "Restaura 60 puntos de vida",
            "type": "consumable",
            "category": "healing",
            "effect": {
                "health": 60
            },
            "target": "self",
            "usable_in": ["combat", "dungeon"],
            "price": 50,
            "rarity": "uncommon",
            "stackable": true,
            "max_stack": 10,
            "icon": "🧪"
        },
        {
            "id": "hp_potion_large",
            "name": "Poción de Vida Grande",
            "description": "Restaura 120 puntos de vida",
            "type": "consumable",
            "category": "healing",
            "effect": {
                "health": 120
            },
            "target": "self",
            "usable_in": ["combat", "dungeon"],
            "price": 100,
            "rarity": "rare",
            "stackable": true,
            "max_stack": 5,
            "icon": "🧪"
        },
        {
            "id": "mp_potion_small",
            "name": "Poción de Maná Pequeña",
            "description": "Restaura 20 puntos de maná",
            "type": "consumable",
            "category": "mana",
            "effect": {
                "mana": 20
            },
            "target": "self",
            "usable_in": ["combat", "dungeon"],
            "price": 20,
            "rarity": "common",
            "stackable": true,
            "max_stack": 10,
            "icon": "💙"
        },
        {
            "id": "mp_potion_medium",
            "name": "Poción de Maná Mediana",
            "description": "Restaura 40 puntos de maná",
            "type": "consumable",
            "category": "mana",
            "effect": {
                "mana": 40
            },
            "target": "self",
            "usable_in": ["combat", "dungeon"],
            "price": 40,
            "rarity": "uncommon",
            "stackable": true,
            "max_stack": 10,
            "icon": "💙"
        },
        {
            "id": "mp_potion_large",
            "name": "Poción de Maná Grande",
            "description": "Restaura 80 puntos de maná (completamente)",
            "type": "consumable",
            "category": "mana",
            "effect": {
                "mana": 80
            },
            "target": "self",
            "usable_in": ["combat", "dungeon"],
            "price": 80,
            "rarity": "rare",
            "stackable": true,
            "max_stack": 5,
            "icon": "💙"
        },
        {
            "id": "antidote",
            "name": "Antídoto",
            "description": "Cura el estado de Envenenado",
            "type": "consumable",
            "category": "cure",
            "effect": {
                "cure_state": "Envenenado"
            },
            "target": "self",
            "usable_in": ["combat", "dungeon"],
            "price": 30,
            "rarity": "common",
            "stackable": true,
            "max_stack": 5,
            "icon": "🍀"
        },
        {
            "id": "burn_salve",
            "name": "Ungüento Frío",
            "description": "Cura el estado de Quemado",
            "type": "consumable",
            "category": "cure",
            "effect": {
                "cure_state": "Quemado"
            },
            "target": "self",
            "usable_in": ["combat", "dungeon"],
            "price": 30,
            "rarity": "common",
            "stackable": true,
            "max_stack": 5,
            "icon": "❄️"
        },
        {
            "id": "bandage",
            "name": "Vendaje",
            "description": "Cura el estado de Sangrado",
            "type": "consumable",
            "category": "cure",
            "effect": {
                "cure_state": "Sangrado"
            },
            "target": "self",
            "usable_in": ["combat", "dungeon"],
            "price": 25,
            "rarity": "common",
            "stackable": true,
            "max_stack": 5,
            "icon": "🩹"
        },
        {
            "id": "courage_potion",
            "name": "Poción de Valor",
            "description": "Cura el estado de Miedo",
            "type": "consumable",
            "category": "cure",
            "effect": {
                "cure_state": "Miedo"
            },
            "target": "self",
            "usable_in": ["combat", "dungeon"],
            "price": 35,
            "rarity": "uncommon",
            "stackable": true,
            "max_stack": 5,
            "icon": "🛡️"
        },
        {
            "id": "bomb",
            "name": "Bomba Pequeña",
            "description": "Inflige 40 de daño al enemigo",
            "type": "consumable",
            "category": "damage",
            "effect": {
                "damage": 40
            },
            "target": "enemy",
            "usable_in": ["combat"],
            "price": 60,
            "rarity": "uncommon",
            "stackable": true,
            "max_stack": 3,
            "icon": "💣"
        },
        {
            "id": "grenade",
            "name": "Granada Explosiva",
            "description": "Inflige 80 de daño al enemigo",
            "type": "consumable",
            "category": "damage",
            "effect": {
                "damage": 80
            },
            "target": "enemy",
            "usable_in": ["combat"],
            "price": 120,
            "rarity": "rare",
            "stackable": true,
            "max_stack": 3,
            "icon": "💥"
        },
        {
            "id": "strength_elixir",
            "name": "Elixir de Fuerza",
            "description": "Aumenta el daño en 15 durante 3 turnos",
            "type": "consumable",
            "category": "buff",
            "effect": {
                "buff": {
                    "stat": "damage",
                    "value": 15,
                    "duration": 3
                }
            },
            "target": "self",
            "usable_in": ["combat"],
            "price": 70,
            "rarity": "uncommon",
            "stackable": true,
            "max_stack": 3,
            "icon": "⚡"
        },
        {
            "id": "defense_elixir",
            "name": "Elixir de Defensa",
            "description": "Reduce daño recibido en 10 durante 3 turnos",
            "type": "consumable",
            "category": "buff",
            "effect": {
                "buff": {
                    "stat": "defense",
                    "value": 10,
                    "duration": 3
                }
            },
            "target": "self",
            "usable_in": ["combat"],
            "price": 70,
            "rarity": "uncommon",
            "stackable": true,
            "max_stack": 3,
            "icon": "🛡️"
        },
        {
            "id": "speed_elixir",
            "name": "Elixir de Velocidad",
            "description": "Aumenta velocidad en 0.3 durante 3 turnos",
            "type": "consumable",
            "category": "buff",
            "effect": {
                "buff": {
                    "stat": "speed",
                    "value": 0.3,
                    "duration": 3
                }
            },
            "target": "self",
            "usable_in": ["combat"],
            "price": 80,
            "rarity": "rare",
            "stackable": true,
            "max_stack": 3,
            "icon": "💨"
        },
        {
            "id": "phoenix_feather",
            "name": "Pluma de Fénix",
            "description": "Revive automáticamente con 50% HP si mueres",
            "type": "consumable",
            "category": "special",
            "effect": {
                "auto_revive": {
                    "health_percent": 0.5
                }
            },
            "target": "self",
            "usable_in": ["combat", "dungeon"],
            "price": 200,
            "rarity": "legendary",
            "stackable": true,
            "max_stack": 1,
            "icon": "🔥"
        },
        {
            "id": "escape_rope",
            "name": "Cuerda de Escape",
            "description": "Garantiza huida exitosa del combate (no funciona contra jefes)",
            "type": "consumable",
            "category": "special",
            "effect": {
                "guaranteed_flee": true
            },
            "target": "self",
            "usable_in": ["combat"],
            "price": 50,
            "rarity": "uncommon",
            "stackable": true,
            "max_stack": 3,
            "icon": "🧵"
        }
    ]
}
```

#### 3.1.2 Clase Item (src/object/item.py)

```python
from dataclasses import dataclass
from typing import Dict, Any, List
import json

@dataclass
class Item:
    """Clase que representa un item del juego."""
    id: str
    name: str
    description: str
    type: str  # consumable, equipment, quest
    category: str  # healing, mana, cure, damage, buff, special
    effect: Dict[str, Any]
    target: str  # self, enemy
    usable_in: List[str]  # combat, dungeon, shop
    price: int
    rarity: str  # common, uncommon, rare, legendary
    stackable: bool
    max_stack: int
    icon: str
    
    def can_use(self, context: str) -> bool:
        """Verifica si el item puede usarse en el contexto actual."""
        return context in self.usable_in
    
    def use(self, target, context: str = "combat") -> tuple[bool, str]:
        """
        Usa el item en el objetivo especificado.
        
        Returns:
            tuple[bool, str]: (success, message)
        """
        if not self.can_use(context):
            return False, f"No puedes usar {self.name} aquí."
        
        message = ""
        
        # Curación de HP
        if "health" in self.effect:
            health_restored = self.effect["health"]
            old_health = target.getHealth()
            target.setHealth(target.getHealth() + health_restored)
            actual_restored = target.getHealth() - old_health
            message = f"Usaste {self.name}. Recuperaste {actual_restored} HP."
        
        # Restauración de MP
        elif "mana" in self.effect:
            if hasattr(target, 'skill_manager'):
                mana_restored = self.effect["mana"]
                old_mana = target.skill_manager.current_mana
                target.skill_manager.current_mana = min(
                    target.skill_manager.max_mana,
                    target.skill_manager.current_mana + mana_restored
                )
                actual_restored = target.skill_manager.current_mana - old_mana
                message = f"Usaste {self.name}. Recuperaste {actual_restored} MP."
            else:
                return False, f"{target.getName()} no puede usar maná."
        
        # Curar estado alterado
        elif "cure_state" in self.effect:
            state_to_cure = self.effect["cure_state"]
            if target.getState() and target.getState().get("state") == state_to_cure:
                target.setState(None)
                message = f"Usaste {self.name}. Curaste el estado {state_to_cure}."
            else:
                return False, f"No estás afectado por {state_to_cure}."
        
        # Daño al enemigo
        elif "damage" in self.effect:
            damage = self.effect["damage"]
            target.setHealth(target.getHealth() - damage)
            message = f"Usaste {self.name}. Infligiste {damage} de daño."
        
        # Buff temporal
        elif "buff" in self.effect:
            buff = self.effect["buff"]
            # Esto requiere un sistema de buffs en MainCharacter
            message = f"Usaste {self.name}. {buff['stat'].capitalize()} aumentado por {buff['duration']} turnos."
        
        # Efectos especiales
        elif "auto_revive" in self.effect:
            # Implementar lógica de auto-revive
            message = f"Usaste {self.name}. Serás revivido si mueres."
        
        elif "guaranteed_flee" in self.effect:
            message = f"Usaste {self.name}. La huida está garantizada."
        
        return True, message
    
    def get_display_name(self) -> str:
        """Retorna el nombre con el icono."""
        return f"{self.icon} {self.name}"


def load_items(json_path: str) -> Dict[str, Item]:
    """
    Carga todos los items desde el archivo JSON.
    
    Returns:
        Dict[str, Item]: Diccionario con {item_id: Item}
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    items = {}
    for category_items in data.values():
        for item_data in category_items:
            item = Item(**item_data)
            items[item.id] = item
    
    return items
```

### 3.2 Sistema de Inventario

#### 3.2.1 Clase InventoryManager (src/inventory_system.py)

```python
from typing import Dict, List, Optional
from src.object.item import Item, load_items
import json

class InventoryManager:
    """Gestor del inventario del jugador."""
    
    def __init__(self, max_slots: int = 30):
        self.max_slots = max_slots
        self.items: Dict[str, int] = {}  # {item_id: quantity}
        self._item_db: Dict[str, Item] = {}  # Cache de items
    
    def load_item_database(self, json_path: str):
        """Carga la base de datos de items."""
        self._item_db = load_items(json_path)
    
    def get_item(self, item_id: str) -> Optional[Item]:
        """Obtiene un item de la base de datos."""
        return self._item_db.get(item_id)
    
    def add_item(self, item_id: str, quantity: int = 1) -> tuple[bool, str]:
        """
        Añade items al inventario.
        
        Returns:
            tuple[bool, str]: (success, message)
        """
        item = self.get_item(item_id)
        if not item:
            return False, f"Item {item_id} no existe."
        
        # Verificar si hay espacio
        if item_id not in self.items and len(self.items) >= self.max_slots:
            return False, "Inventario lleno."
        
        # Verificar límite de stack
        current = self.items.get(item_id, 0)
        if item.stackable:
            if current + quantity > item.max_stack:
                return False, f"No puedes tener más de {item.max_stack} {item.name}."
        else:
            if current > 0:
                return False, f"{item.name} no es apilable."
        
        self.items[item_id] = current + quantity
        return True, f"Añadido {quantity}x {item.name}."
    
    def remove_item(self, item_id: str, quantity: int = 1) -> tuple[bool, str]:
        """Remueve items del inventario."""
        if item_id not in self.items:
            return False, "No tienes ese item."
        
        current = self.items[item_id]
        if current < quantity:
            return False, f"Solo tienes {current} de ese item."
        
        self.items[item_id] -= quantity
        if self.items[item_id] <= 0:
            del self.items[item_id]
        
        item = self.get_item(item_id)
        return True, f"Usado {quantity}x {item.name if item else item_id}."
    
    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        """Verifica si el inventario tiene suficiente cantidad de un item."""
        return self.items.get(item_id, 0) >= quantity
    
    def use_item(self, item_id: str, target, context: str = "combat") -> tuple[bool, str]:
        """
        Usa un item del inventario.
        
        Returns:
            tuple[bool, str]: (success, message)
        """
        if not self.has_item(item_id):
            return False, "No tienes ese item."
        
        item = self.get_item(item_id)
        if not item:
            return False, "Item no válido."
        
        success, message = item.use(target, context)
        if success:
            self.remove_item(item_id, 1)
        
        return success, message
    
    def get_items_by_category(self, category: str) -> List[tuple[Item, int]]:
        """Obtiene todos los items de una categoría."""
        result = []
        for item_id, quantity in self.items.items():
            item = self.get_item(item_id)
            if item and item.category == category:
                result.append((item, quantity))
        return result
    
    def get_usable_items(self, context: str = "combat") -> List[tuple[Item, int]]:
        """Obtiene todos los items usables en el contexto actual."""
        result = []
        for item_id, quantity in self.items.items():
            item = self.get_item(item_id)
            if item and item.can_use(context):
                result.append((item, quantity))
        return result
    
    def get_total_slots_used(self) -> int:
        """Retorna el número de slots ocupados."""
        return len(self.items)
    
    def to_dict(self) -> Dict:
        """Convierte el inventario a diccionario para guardado."""
        return {
            "max_slots": self.max_slots,
            "items": self.items
        }
    
    def from_dict(self, data: Dict):
        """Carga el inventario desde un diccionario."""
        self.max_slots = data.get("max_slots", 30)
        self.items = data.get("items", {})


def get_inventory_manager() -> InventoryManager:
    """Singleton del gestor de inventario."""
    if not hasattr(get_inventory_manager, "_instance"):
        get_inventory_manager._instance = InventoryManager()
    return get_inventory_manager._instance
```

### 3.3 Sistema de Turnos

#### 3.3.1 Flujo del Sistema de Turnos

```
┌─────────────────────────────────────────────┐
│         INICIO DEL COMBATE                  │
│  1. Calcular orden de turnos                │
│     (basado en velocidad de ambos)          │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│     ¿Es turno del jugador?                  │
└─────┬───────────────────────────────┬───────┘
      │ SÍ                            │ NO
      ▼                               ▼
┌─────────────────────┐    ┌──────────────────────┐
│ MOSTRAR MENÚ        │    │ TURNO DEL ENEMIGO    │
│ ┌─────────────────┐ │    │ - IA decide acción   │
│ │ > Atacar        │ │    │ - Ejecuta ataque     │
│ │   Habilidad     │ │    │ - Aplica efectos     │
│ │   Item          │ │    │ - Animar             │
│ │   Huir          │ │    │ - Actualizar HP      │
│ └─────────────────┘ │    └──────────┬───────────┘
└─────────┬───────────┘               │
          │                           │
          ▼                           │
┌─────────────────────────────────┐   │
│ JUGADOR SELECCIONA ACCIÓN       │   │
└─────┬───────────────────────────┘   │
      │                               │
      ▼                               │
┌─────────────────────────┐           │
│ ¿ATACAR?                │           │
│ - Calcular daño         │           │
│ - Aplicar a enemigo     │           │
│ - animation_player_atack│           │
└─────────┬───────────────┘           │
          │                           │
          ▼                           │
┌─────────────────────────┐           │
│ ¿HABILIDAD?             │           │
│ - Mostrar submenú       │           │
│ - Verificar maná        │           │
│ - Verificar cooldown    │           │
│ - Ejecutar habilidad    │           │
│ - Actualizar cooldowns  │           │
└─────────┬───────────────┘           │
          │                           │
          ▼                           │
┌─────────────────────────┐           │
│ ¿ITEM?                  │           │
│ - Mostrar inventario    │           │
│ - Seleccionar item      │           │
│ - Usar item             │           │
│ - Remover de inventario │           │
└─────────┬───────────────┘           │
          │                           │
          ▼                           │
┌─────────────────────────┐           │
│ ¿HUIR?                  │           │
│ - Calcular probabilidad │           │
│ - Si falla: enemigo     │           │
│   ataca gratis          │           │
│ - Si éxito: fin combate │           │
└─────────┬───────────────┘           │
          │                           │
          ▼◄──────────────────────────┘
┌─────────────────────────────────────────────┐
│  ACTUALIZAR ESTADO                          │
│  - Regenerar maná (+10)                     │
│  - Reducir cooldowns (-1)                   │
│  - Procesar buffs activos                   │
│  - Procesar estados alterados               │
│  - Actualizar UI                            │
└─────────┬───────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────┐
│  ¿COMBATE TERMINADO?                        │
│  - Jugador HP <= 0: DERROTA                 │
│  - Enemigo HP <= 0: VICTORIA                │
│  - Huida exitosa: HUIDA                     │
└─────┬──────────────────────────┬────────────┘
      │ NO                       │ SÍ
      │                          │
      │ ◄────────────────────┐   │
      └─► SIGUIENTE TURNO    │   │
              │              │   │
              └──────────────┘   │
                                 ▼
                           FIN DEL COMBATE
```

#### 3.3.2 Clase CombatManager (levels/combat_manager.py)

```python
from typing import Literal
from collections import deque

class CombatManager:
    """Gestor del sistema de combate por turnos."""
    
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn_count = 0
        self.combat_active = True
        self.turn_queue = deque()
        self.player_buffs = []  # Lista de buffs activos
        self.enemy_buffs = []
        
        # Calcular orden inicial de turnos
        self._calculate_turn_order()
    
    def _calculate_turn_order(self):
        """
        Calcula el orden de turnos basado en velocidad.
        Un personaje más rápido puede atacar múltiples veces.
        """
        player_speed = self.player.getWeapon()["attack_ratio"]
        enemy_speed = self.enemy.getAttackRate()
        
        # Sistema simple: el más rápido va primero
        # Si la diferencia es > 0.3, el rápido ataca 2 veces
        speed_diff = abs(player_speed - enemy_speed)
        
        if player_speed > enemy_speed:
            self.turn_queue.append("player")
            if speed_diff >= 0.3:
                self.turn_queue.append("player")
            self.turn_queue.append("enemy")
        else:
            self.turn_queue.append("enemy")
            if speed_diff >= 0.3:
                self.turn_queue.append("enemy")
            self.turn_queue.append("player")
    
    def get_current_turn(self) -> Literal["player", "enemy"]:
        """Retorna de quién es el turno actual."""
        if not self.turn_queue:
            self._calculate_turn_order()
        return self.turn_queue[0]
    
    def end_turn(self):
        """Finaliza el turno actual y pasa al siguiente."""
        if self.turn_queue:
            self.turn_queue.popleft()
        
        if not self.turn_queue:
            # Nuevo ciclo de turnos
            self.turn_count += 1
            self._calculate_turn_order()
            self._process_turn_effects()
    
    def _process_turn_effects(self):
        """Procesa efectos al final de cada ciclo completo."""
        # Regenerar maná del jugador
        if hasattr(self.player, 'skill_manager'):
            self.player.skill_manager.regenerate_mana()
            self.player.skill_manager.update_cooldowns()
        
        # Procesar buffs activos
        self._update_buffs(self.player_buffs)
        self._update_buffs(self.enemy_buffs)
        
        # Procesar estados alterados
        self._process_states()
    
    def _update_buffs(self, buff_list):
        """Actualiza la duración de los buffs."""
        for buff in buff_list[:]:
            buff["duration"] -= 1
            if buff["duration"] <= 0:
                buff_list.remove(buff)
    
    def _process_states(self):
        """Procesa daño/efectos de estados alterados."""
        # Estados del jugador (envenenado, quemado, etc.)
        if self.player.getState():
            state = self.player.getState()
            if "effect" in state and "health" in state["effect"]:
                damage = state["effect"]["health"]
                self.player.setHealth(self.player.getHealth() + damage)
        
        # Estados del enemigo
        if self.enemy.getState():
            state = self.enemy.getState()
            if "effect" in state and "health" in state["effect"]:
                damage = state["effect"]["health"]
                self.enemy.setHealth(self.enemy.getHealth() + damage)
    
    def calculate_flee_chance(self) -> float:
        """Calcula la probabilidad de huida."""
        level_diff = self.player.getLevel() - self.enemy.level_max
        base_chance = 50  # 50% base
        
        # +5% por cada nivel de diferencia
        chance = base_chance + (level_diff * 5)
        
        # Limitar entre 10% y 90%
        return max(10, min(90, chance))
    
    def is_combat_over(self) -> tuple[bool, Literal["victory", "defeat", "flee", None]]:
        """
        Verifica si el combate ha terminado.
        
        Returns:
            tuple[bool, str]: (is_over, result)
        """
        if self.player.getHealth() <= 0:
            return True, "defeat"
        if self.enemy.getHealth() <= 0:
            return True, "victory"
        if not self.combat_active:
            return True, "flee"
        return False, None
```

### 3.4 UI de Combate Mejorada

#### 3.4.1 Mockup ASCII

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  [Guerrero]         HP: ████████░░ 80/100     [Goblin]        │ Y=100
│                     MP: ██████░░░░ 60/100                      │ Y=125
│                                                HP: █████░░░░░  │ Y=150
│                                                   50/100       │
│                                                                │
│            🧙            COMBATE           👹                 │
│         [Animación]                    [Animación]            │ Y=250
│                                                                │
│                                                                │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│  [Combat Message Box]                                         │ Y=450
│  > El Goblin te atacó por 15 de daño.                        │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│  ┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┓                  │ Y=530
│  ┃ >Atacar ┃ Habilidad ┃  Item   ┃  Huir   ┃                  │
│  ┗━━━━━━━━━┻━━━━━━━━━━━┻━━━━━━━━━┻━━━━━━━━━┛                  │
└────────────────────────────────────────────────────────────────┘ Y=600
```

#### 3.4.2 Coordenadas y Espaciado

```python
# Constantes de UI para draw_combat_scene()
UI_LEFT_X = 50
UI_RIGHT_X = 550
NAME_Y = 100
HP_BAR_Y = 125
MP_BAR_Y = 150  # Solo para jugador
BAR_WIDTH = 200
BAR_HEIGHT = 16

COMBAT_MESSAGE_BOX_Y = 450
COMBAT_MESSAGE_BOX_HEIGHT = 70

ACTIONS_MENU_Y = 530
ACTIONS_MENU_HEIGHT = 60
```

---

## 4. 🔧 PLAN DE IMPLEMENTACIÓN

### Fase 1: ✅ Análisis y Diseño (COMPLETADA)
- Análisis de código actual
- Diseño de estructura de datos
- Diseño de flujos
- Mockups de UI

### Fase 2: Base de Datos e Inventario (2h)
- **BackendJunior**: Crear `itemsDb.json` con 17 items
- **BackendJunior**: Implementar clase `Item`
- **BackendSenior**: Implementar `InventoryManager`
- **BackendSenior**: Integrar con `MainCharacter`

### Fase 3: Tienda Ampliada (1.5h)
- **FrontendJunior**: Añadir sección de items a tienda
- **Designer**: Diseñar layout de tienda mejorado
- **FrontendSenior**: Revisar y optimizar

### Fase 4: Sistema de Turnos (3h)
- **GameDevSenior**: Implementar `CombatManager`
- **GameDevJunior**: Crear menú de acciones
- **GameDevSenior**: Integrar habilidades en combate
- **GameDevJunior**: Implementar sistema de huida

### Fase 5: UI Mejorada (1.8h)
- **FrontendSenior**: Reposicionar elementos existentes
- **FrontendJunior**: Crear menú de acciones
- **GameDevSenior**: Adaptar animaciones a turnos
- **FrontendJunior**: Integrar combat_message_box

### Fase 6: Integración (2h)
- **GameDevSenior**: Integrar logros en combate
- **BackendSenior**: Actualizar sistema de guardado
- **FrontendJunior**: Crear selector de slots

### Fase 7: Testing (1.5h)
- **QA**: Tests unitarios
- **GameDevSenior**: Balanceo
- **QA**: Playtesting

### Fase 8: Documentación (1h)
- **DocWriter**: Actualizar README
- **DocWriter**: Completar docstrings

**Total: ~13.8 horas**

---

## 5. 📋 CRITERIOS DE ACEPTACIÓN

### Funcionales
- [ ] El jugador puede elegir entre 4 acciones en su turno
- [ ] Las habilidades consumen maná y tienen cooldowns
- [ ] Los items se usan desde el inventario y tienen efectos visibles
- [ ] El sistema de huida funciona con probabilidad balanceada
- [ ] Los turnos se calculan correctamente según velocidad
- [ ] Las animaciones se ejecutan en el momento correcto

### Técnicos
- [ ] Código modular y bien documentado
- [ ] Sin duplicación de lógica
- [ ] Tests unitarios al 100%
- [ ] Guardado incluye inventario y cooldowns
- [ ] No hay regresiones en funcionalidad existente

### UX/UI
- [ ] La UI es clara y no abruma
- [ ] El combate tiene buen ritmo (no muy lento)
- [ ] Los mensajes son informativos
- [ ] Las animaciones no bloquean innecesariamente
- [ ] El menú es fácil de navegar

---

## 6. 🎮 EJEMPLO DE FLUJO COMPLETO

### Escenario: Combate contra un Goblin

```
1. INICIO DEL COMBATE
   - Player (Velocidad: 0.7) vs Goblin (Velocidad: 0.5)
   - Orden: Player → Player → Enemy (diferencia > 0.3)
   - Animación de inicio de combate

2. TURNO 1 - JUGADOR
   UI muestra:
   [Guerrero] HP: ████████░░ 80/100  MP: ██████░░░░ 60/100
   [Goblin]   HP: █████░░░░░ 50/100
   
   Menú: > [Atacar] | Habilidad | Item | Huir
   
   → Jugador selecciona "Habilidad"
   
   Submenú:
   > Golpe Poderoso (20 MP) [Disponible]
     Segundo Aliento (15 MP) [Cooldown: 2]
     Carga Frenética (25 MP) [Disponible]
   
   → Selecciona "Golpe Poderoso"
   
   - animation_player_atack()
   - Daño: 45
   - MP: 60 → 40
   - combat_message_box: "¡Golpe Poderoso! 45 de daño."
   - Goblin HP: 50 → 5
   
3. TURNO 2 - JUGADOR (doble turno)
   Menú: > [Atacar] | Habilidad | Item | Huir
   
   → Jugador selecciona "Atacar"
   
   - animation_player_atack()
   - Daño: 12
   - combat_message_box: "Golpe crítico! 12 de daño."
   - Goblin HP: 5 → 0
   
4. VICTORIA
   - animation_victory()
   - combat_message_box: "¡Victoria! +30 EXP, +40 Oro"
   - toast_manager: "¡Logro desbloqueado: Primera Victoria!"
   
5. FIN DEL COMBATE
   - Guardar progreso
   - Volver a exploración
```

---

## 7. 🚨 RIESGOS Y MITIGACIONES

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Romper animaciones existentes | Media | Alto | Testear exhaustivamente, mantener funciones originales |
| Balance incorrecto de items | Alta | Medio | Playtesting extensivo, ajuste iterativo |
| Inventario lleno bloquea gameplay | Media | Alto | Implementar venta/descarte de items |
| Combate por turnos demasiado lento | Media | Alto | Optimizar animaciones, permitir skip |
| Conflictos con sistema de guardado | Baja | Alto | Tests de integración, backups automáticos |

---

## 8. 📊 MÉTRICAS DE ÉXITO

- **Tiempo de combate promedio**: 30-60 segundos
- **Uso de items**: Al menos 70% de jugadores usan items en combate
- **Tasa de huida**: 15-25% de combates terminan en huida
- **Uso de habilidades**: Al menos 50% de combates incluyen uso de habilidades
- **Tests pasados**: 100%
- **Bugs críticos**: 0

---

**Documento aprobado por:** PM + GameDevSenior  
**Fecha de aprobación:** 24 de enero de 2026  
**Próximo paso:** Iniciar Fase 2 - Implementación de Items e Inventario
