"""
Sistema de Inventario para Cursed Dungeon.

Este módulo implementa el gestor de inventario del jugador con soporte para
items apilables, límites de slots, y persistencia.
"""

from typing import Dict, List, Optional, Tuple
from src.object.item import Item, load_items
from src.others import resource_path
import json


class InventoryManager:
    """Gestor del inventario del jugador."""
    
    def __init__(self, max_slots: int = 30):
        """
        Inicializa el inventario.
        
        Args:
            max_slots: Número máximo de slots diferentes (tipos de items)
        """
        self.max_slots = max_slots
        self.items: Dict[str, int] = {}  # {item_id: quantity}
        self._item_db: Dict[str, Item] = {}  # Cache de items
    
    def load_item_database(self, json_path: str = None):
        """
        Carga la base de datos de items.
        
        Args:
            json_path: Ruta al archivo itemsDb.json (opcional)
        """
        if json_path is None:
            json_path = resource_path("src/db/itemsDb.json")
        
        self._item_db = load_items(json_path)
        print(f"[InventoryManager] Cargados {len(self._item_db)} items.")
    
    def get_item(self, item_id: str) -> Optional[Item]:
        """
        Obtiene un item de la base de datos.
        
        Args:
            item_id: ID del item
        
        Returns:
            Item o None si no existe
        """
        return self._item_db.get(item_id)
    
    def add_item(self, item_id: str, quantity: int = 1) -> Tuple[bool, str]:
        """
        Añade items al inventario.
        
        Args:
            item_id: ID del item a añadir
            quantity: Cantidad a añadir
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        item = self.get_item(item_id)
        if not item:
            return False, f"Item {item_id} no existe."
        
        # Verificar si hay espacio (solo si es un nuevo tipo de item)
        if item_id not in self.items and len(self.items) >= self.max_slots:
            return False, "Inventario lleno. Vende o descarta items."
        
        # Verificar límite de stack
        current = self.items.get(item_id, 0)
        if item.stackable:
            if current + quantity > item.max_stack:
                return False, f"No puedes tener más de {item.max_stack} {item.name}."
        else:
            if current > 0:
                return False, f"{item.name} no es apilable."
        
        self.items[item_id] = current + quantity
        return True, f"Añadido {quantity}x {item.get_display_name()}."
    
    def remove_item(self, item_id: str, quantity: int = 1) -> Tuple[bool, str]:
        """
        Remueve items del inventario.
        
        Args:
            item_id: ID del item a remover
            quantity: Cantidad a remover
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        if item_id not in self.items:
            return False, "No tienes ese item."
        
        current = self.items[item_id]
        if current < quantity:
            return False, f"Solo tienes {current} de ese item."
        
        self.items[item_id] -= quantity
        if self.items[item_id] <= 0:
            del self.items[item_id]
        
        item = self.get_item(item_id)
        item_name = item.name if item else item_id
        return True, f"Removido {quantity}x {item_name}."
    
    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        """
        Verifica si el inventario tiene suficiente cantidad de un item.
        
        Args:
            item_id: ID del item
            quantity: Cantidad requerida
        
        Returns:
            bool: True si tiene suficiente, False si no
        """
        return self.items.get(item_id, 0) >= quantity
    
    def use_item(self, item_id: str, target, context: str = "combat") -> Tuple[bool, str]:
        """
        Usa un item del inventario en un objetivo.
        
        Args:
            item_id: ID del item a usar
            target: Objetivo del item (MainCharacter o Enemy)
            context: Contexto de uso ('combat', 'dungeon')
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        if not self.has_item(item_id):
            return False, "No tienes ese item."
        
        item = self.get_item(item_id)
        if not item:
            return False, "Item no válido."
        
        # Intentar usar el item
        success, message = item.use(target, context)
        
        # Solo remover del inventario si se usó exitosamente
        if success:
            self.remove_item(item_id, 1)
        
        return success, message
    
    def get_items_by_category(self, category: str) -> List[Tuple[Item, int]]:
        """
        Obtiene todos los items de una categoría específica.
        
        Args:
            category: Categoría a filtrar ('healing', 'mana', 'cure', etc.)
        
        Returns:
            List[Tuple[Item, int]]: Lista de (item, quantity)
        """
        result = []
        for item_id, quantity in self.items.items():
            item = self.get_item(item_id)
            if item and item.category == category:
                result.append((item, quantity))
        return result
    
    def get_usable_items(self, context: str = "combat") -> List[Tuple[Item, int]]:
        """
        Obtiene todos los items usables en el contexto actual.
        
        Args:
            context: Contexto actual ('combat', 'dungeon')
        
        Returns:
            List[Tuple[Item, int]]: Lista de (item, quantity)
        """
        result = []
        for item_id, quantity in self.items.items():
            item = self.get_item(item_id)
            if item and item.can_use(context):
                result.append((item, quantity))
        return result
    
    def get_all_items(self) -> List[Tuple[Item, int]]:
        """
        Obtiene todos los items del inventario.
        
        Returns:
            List[Tuple[Item, int]]: Lista de (item, quantity)
        """
        result = []
        for item_id, quantity in self.items.items():
            item = self.get_item(item_id)
            if item:
                result.append((item, quantity))
        return result
    
    def get_total_slots_used(self) -> int:
        """
        Retorna el número de slots ocupados (tipos de items diferentes).
        
        Returns:
            int: Número de slots ocupados
        """
        return len(self.items)
    
    def get_slots_remaining(self) -> int:
        """
        Retorna el número de slots disponibles.
        
        Returns:
            int: Número de slots libres
        """
        return self.max_slots - len(self.items)
    
    def is_full(self) -> bool:
        """
        Verifica si el inventario está lleno.
        
        Returns:
            bool: True si está lleno, False si no
        """
        return len(self.items) >= self.max_slots
    
    def clear(self):
        """Vacía el inventario completamente."""
        self.items.clear()
    
    def to_dict(self) -> Dict:
        """
        Convierte el inventario a diccionario para guardado.
        
        Returns:
            Dict: Datos del inventario serializables
        """
        return {
            "max_slots": self.max_slots,
            "items": self.items
        }
    
    def from_dict(self, data: Dict):
        """
        Carga el inventario desde un diccionario.
        
        Args:
            data: Diccionario con datos del inventario
        """
        self.max_slots = data.get("max_slots", 30)
        self.items = data.get("items", {})
    
    def get_total_value(self) -> int:
        """
        Calcula el valor total de todos los items del inventario.
        
        Returns:
            int: Valor total en oro
        """
        total = 0
        for item_id, quantity in self.items.items():
            item = self.get_item(item_id)
            if item:
                total += item.price * quantity
        return total
    
    def __repr__(self) -> str:
        """Representación en string del inventario."""
        return f"<InventoryManager: {len(self.items)}/{self.max_slots} slots>"


# Singleton para acceso global
_inventory_manager_instance = None


def get_inventory_manager() -> InventoryManager:
    """
    Retorna la instancia única del gestor de inventario (Singleton).
    
    Returns:
        InventoryManager: Instancia del gestor
    """
    global _inventory_manager_instance
    if _inventory_manager_instance is None:
        _inventory_manager_instance = InventoryManager()
        # Intentar cargar la base de datos automáticamente
        try:
            _inventory_manager_instance.load_item_database()
        except Exception as e:
            print(f"[InventoryManager] Advertencia: No se pudo cargar itemsDb.json: {e}")
    
    return _inventory_manager_instance


def reset_inventory_manager():
    """Resetea el singleton (útil para testing)."""
    global _inventory_manager_instance
    _inventory_manager_instance = None
