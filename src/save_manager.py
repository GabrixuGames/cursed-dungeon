"""
Sistema de gestión de guardado con múltiples slots.
Permite guardar hasta 3 partidas diferentes con metadata.
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional


class SaveManager:
    """Gestor centralizado para guardado y carga de partidas."""
    
    MAX_SLOTS = 3
    SAVE_DIR = "saves"
    
    def __init__(self):
        """Inicializa el gestor de guardado."""
        self._ensure_save_directory()
    
    def _ensure_save_directory(self):
        """Crea el directorio de guardado si no existe."""
        if not os.path.exists(self.SAVE_DIR):
            try:
                os.makedirs(self.SAVE_DIR)
            except OSError as e:
                print(f"Error creating save directory: {e}")
    
    def get_save_path(self, slot: int) -> str:
        """Retorna la ruta del archivo de guardado para un slot."""
        return os.path.join(self.SAVE_DIR, f"save_slot_{slot}.json")
    
    def get_backup_path(self, slot: int) -> str:
        """Retorna la ruta del backup para un slot."""
        return self.get_save_path(slot) + ".backup"
    
    def save_game(self, slot: int, character_data: Dict) -> bool:
        """
        Guarda los datos del personaje en el slot especificado.
        
        Args:
            slot: Número de slot (1-3)
            character_data: Diccionario con los datos del personaje
            
        Returns:
            True si el guardado fue exitoso, False en caso contrario
        """
        if not 1 <= slot <= self.MAX_SLOTS:
            print(f"Invalid slot number: {slot}. Must be between 1 and {self.MAX_SLOTS}")
            return False
        
        save_path = self.get_save_path(slot)
        backup_path = self.get_backup_path(slot)
        
        try:
            # Añadir metadata
            save_data = {
                "metadata": {
                    "slot": slot,
                    "save_date": datetime.now().isoformat(),
                    "timestamp": time.time(),
                    "version": "0.3"
                },
                "character": character_data
            }
            
            # Crear backup del guardado existente
            if os.path.exists(save_path):
                try:
                    with open(save_path, 'r', encoding='utf-8') as f:
                        backup_data = json.load(f)
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        json.dump(backup_data, f, indent=2, ensure_ascii=False)
                except Exception as e:
                    print(f"Warning: Could not create backup: {e}")
            
            # Guardar datos
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            # Eliminar backup si el guardado fue exitoso
            if os.path.exists(backup_path):
                try:
                    os.remove(backup_path)
                except OSError:
                    pass  # El backup puede quedarse si falla la eliminación
            
            return True
            
        except Exception as e:
            print(f"Error saving game to slot {slot}: {e}")
            # Restaurar backup si el guardado falló
            if os.path.exists(backup_path):
                try:
                    os.rename(backup_path, save_path)
                    print("Backup restored due to save failure")
                except OSError:
                    pass
            return False
    
    def load_game(self, slot: int) -> Optional[Dict]:
        """
        Carga los datos del personaje desde el slot especificado.
        
        Args:
            slot: Número de slot (1-3)
            
        Returns:
            Diccionario con los datos del personaje o None si falla
        """
        if not 1 <= slot <= self.MAX_SLOTS:
            print(f"Invalid slot number: {slot}. Must be between 1 and {self.MAX_SLOTS}")
            return None
        
        save_path = self.get_save_path(slot)
        
        try:
            if not os.path.exists(save_path):
                return None
            
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # Validar estructura básica
            if "character" not in save_data:
                raise ValueError("Invalid save file structure")
            
            character_data = save_data["character"]
            
            # Validar campos requeridos
            required_fields = ["name", "level", "damage", "health", "evade_chance",
                             "experience", "money", "atributes", "weapon"]
            
            for field in required_fields:
                if field not in character_data:
                    raise KeyError(f"Missing required field: {field}")
            
            return character_data
            
        except json.JSONDecodeError:
            print(f"Corrupted save file in slot {slot}, attempting backup...")
            return self._load_from_backup(slot)
        
        except Exception as e:
            print(f"Error loading game from slot {slot}: {e}")
            return None
    
    def _load_from_backup(self, slot: int) -> Optional[Dict]:
        """Intenta cargar desde el archivo de backup."""
        backup_path = self.get_backup_path(slot)
        
        try:
            if not os.path.exists(backup_path):
                return None
            
            with open(backup_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            if "character" in save_data:
                print(f"Successfully loaded from backup for slot {slot}")
                return save_data["character"]
            
            return None
            
        except Exception as e:
            print(f"Failed to load backup: {e}")
            return None
    
    def get_save_info(self, slot: int) -> Optional[Dict]:
        """
        Obtiene información del guardado sin cargar todos los datos.
        
        Args:
            slot: Número de slot (1-3)
            
        Returns:
            Diccionario con metadata o None si el slot está vacío
        """
        save_path = self.get_save_path(slot)
        
        try:
            if not os.path.exists(save_path):
                return None
            
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            if "metadata" not in save_data or "character" not in save_data:
                return None
            
            char = save_data["character"]
            meta = save_data["metadata"]
            
            return {
                "slot": slot,
                "name": char.get("name", "Unknown"),
                "level": char.get("level", 1),
                "save_date": meta.get("save_date", "Unknown"),
                "version": meta.get("version", "Unknown")
            }
            
        except Exception as e:
            print(f"Error reading save info from slot {slot}: {e}")
            return None
    
    def list_all_saves(self) -> List[Dict]:
        """
        Lista información de todos los slots de guardado.
        
        Returns:
            Lista de diccionarios con información de cada slot
        """
        saves = []
        for slot in range(1, self.MAX_SLOTS + 1):
            info = self.get_save_info(slot)
            if info:
                saves.append(info)
            else:
                saves.append({
                    "slot": slot,
                    "name": "Empty Slot",
                    "level": 0,
                    "save_date": None,
                    "version": None
                })
        return saves
    
    def delete_save(self, slot: int) -> bool:
        """
        Elimina el guardado del slot especificado.
        
        Args:
            slot: Número de slot (1-3)
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        if not 1 <= slot <= self.MAX_SLOTS:
            return False
        
        save_path = self.get_save_path(slot)
        backup_path = self.get_backup_path(slot)
        
        try:
            if os.path.exists(save_path):
                os.remove(save_path)
            if os.path.exists(backup_path):
                os.remove(backup_path)
            return True
        except Exception as e:
            print(f"Error deleting save from slot {slot}: {e}")
            return False
    
    def slot_exists(self, slot: int) -> bool:
        """Verifica si existe un guardado en el slot especificado."""
        return os.path.exists(self.get_save_path(slot))


# Instancia global del gestor de guardado
_save_manager = None


def get_save_manager() -> SaveManager:
    """Obtiene la instancia global del SaveManager."""
    global _save_manager
    if _save_manager is None:
        _save_manager = SaveManager()
    return _save_manager
