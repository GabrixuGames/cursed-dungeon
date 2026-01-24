"""
Sistema de Items para Cursed Dungeon.

Este módulo define la clase Item y funciones para cargar items desde JSON.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Tuple
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
        """
        Verifica si el item puede usarse en el contexto actual.
        
        Args:
            context: El contexto donde se intenta usar ('combat', 'dungeon', 'shop')
        
        Returns:
            bool: True si puede usarse, False si no
        """
        return context in self.usable_in
    
    def use(self, target, context: str = "combat") -> Tuple[bool, str]:
        """
        Usa el item en el objetivo especificado.
        
        Args:
            target: El objetivo del item (MainCharacter o Enemy)
            context: El contexto donde se usa el item
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        if not self.can_use(context):
            return False, f"No puedes usar {self.name} aquí."
        
        message = ""
        
        # Curación de HP
        if "health" in self.effect:
            health_restored = self.effect["health"]
            old_health = target.getHealth()
            max_health = getattr(target, '_max_health', None)
            
            # Calcular nueva salud sin exceder el máximo
            if max_health:
                new_health = min(old_health + health_restored, max_health)
            else:
                new_health = old_health + health_restored
            
            target.setHealth(new_health)
            actual_restored = new_health - old_health
            message = f"Usaste {self.name}. Recuperaste {int(actual_restored)} HP."
        
        # Restauración de MP
        elif "mana" in self.effect:
            if hasattr(target, 'skill_manager') and target.skill_manager:
                mana_restored = self.effect["mana"]
                old_mana = target.skill_manager.current_mana
                target.skill_manager.current_mana = min(
                    target.skill_manager.max_mana,
                    target.skill_manager.current_mana + mana_restored
                )
                actual_restored = target.skill_manager.current_mana - old_mana
                message = f"Usaste {self.name}. Recuperaste {int(actual_restored)} MP."
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
            # Añadir buff a la lista de buffs activos del personaje
            if not hasattr(target, '_active_buffs'):
                target._active_buffs = []
            
            target._active_buffs.append({
                'stat': buff['stat'],
                'value': buff['value'],
                'duration': buff['duration'],
                'source': self.name
            })
            
            message = f"Usaste {self.name}. {buff['stat'].capitalize()} aumentado por {buff['duration']} turnos."
        
        # Efectos especiales
        elif "auto_revive" in self.effect:
            # Marcar que el personaje tiene auto-revive activo
            if not hasattr(target, '_auto_revive'):
                target._auto_revive = None
            target._auto_revive = self.effect["auto_revive"]
            message = f"Usaste {self.name}. Serás revivido automáticamente si mueres."
        
        elif "guaranteed_flee" in self.effect:
            # Este efecto será verificado por el sistema de combate
            if not hasattr(target, '_guaranteed_flee'):
                target._guaranteed_flee = False
            target._guaranteed_flee = True
            message = f"Usaste {self.name}. La huida está garantizada."
        
        else:
            return False, f"Efecto de {self.name} no implementado."
        
        return True, message
    
    def get_display_name(self) -> str:
        """
        Retorna el nombre con el icono para mostrar en UI.
        
        Returns:
            str: Nombre formateado con icono
        """
        return f"{self.icon} {self.name}"
    
    def get_rarity_color(self) -> str:
        """
        Retorna un código de color según la rareza (para UI).
        
        Returns:
            str: Nombre del color
        """
        rarity_colors = {
            'common': 'white',
            'uncommon': 'green',
            'rare': 'blue',
            'legendary': 'gold'
        }
        return rarity_colors.get(self.rarity, 'white')


def load_items(json_path: str) -> Dict[str, Item]:
    """
    Carga todos los items desde el archivo JSON.
    
    Args:
        json_path: Ruta al archivo itemsDb.json
    
    Returns:
        Dict[str, Item]: Diccionario con {item_id: Item}
    
    Raises:
        FileNotFoundError: Si el archivo no existe
        json.JSONDecodeError: Si el JSON está mal formado
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {json_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error al leer JSON: {e}")
        return {}
    
    items = {}
    for category_items in data.values():
        for item_data in category_items:
            try:
                item = Item(**item_data)
                items[item.id] = item
            except TypeError as e:
                print(f"Error al crear item {item_data.get('id', 'unknown')}: {e}")
                continue
    
    return items


def get_items_by_category(items: Dict[str, Item], category: str) -> List[Item]:
    """
    Filtra items por categoría.
    
    Args:
        items: Diccionario de items
        category: Categoría a filtrar
    
    Returns:
        List[Item]: Lista de items de esa categoría
    """
    return [item for item in items.values() if item.category == category]


def get_items_by_rarity(items: Dict[str, Item], rarity: str) -> List[Item]:
    """
    Filtra items por rareza.
    
    Args:
        items: Diccionario de items
        rarity: Rareza a filtrar
    
    Returns:
        List[Item]: Lista de items de esa rareza
    """
    return [item for item in items.values() if item.rarity == rarity]
