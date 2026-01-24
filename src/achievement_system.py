"""
Sistema de logros (achievements) para Cursed Dungeon.
Trackea progreso del jugador y desbloquea recompensas.
"""

import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Achievement:
    """Representa un logro del juego."""
    id: str
    name: str
    description: str
    category: str  # "combat", "exploration", "progression", "collection", "special"
    requirement: Dict
    reward: Dict  # {"type": "gold/exp/item", "amount": value}
    unlocked: bool = False
    unlock_date: Optional[str] = None
    progress: int = 0
    progress_max: int = 1
    hidden: bool = False  # Logros secretos


class AchievementManager:
    """Gestor del sistema de logros."""
    
    def __init__(self):
        self.achievements = self._initialize_achievements()
        self.save_file = "achievements.json"
        self.load_progress()
    
    def _initialize_achievements(self) -> Dict[str, Achievement]:
        """Inicializa todos los logros del juego."""
        return {
            # Logros de combate
            "first_blood": Achievement(
                id="first_blood",
                name="Primera Sangre",
                description="Derrota a tu primer enemigo",
                category="combat",
                requirement={"enemies_defeated": 1},
                reward={"type": "gold", "amount": 50},
                progress_max=1
            ),
            "slayer_10": Achievement(
                id="slayer_10",
                name="Cazador Novato",
                description="Derrota 10 enemigos",
                category="combat",
                requirement={"enemies_defeated": 10},
                reward={"type": "gold", "amount": 100},
                progress_max=10
            ),
            "slayer_50": Achievement(
                id="slayer_50",
                name="Guerrero Experimentado",
                description="Derrota 50 enemigos",
                category="combat",
                requirement={"enemies_defeated": 50},
                reward={"type": "gold", "amount": 300},
                progress_max=50
            ),
            "slayer_100": Achievement(
                id="slayer_100",
                name="Maestro del Combate",
                description="Derrota 100 enemigos",
                category="combat",
                requirement={"enemies_defeated": 100},
                reward={"type": "gold", "amount": 1000},
                progress_max=100
            ),
            "perfect_dodge": Achievement(
                id="perfect_dodge",
                name="Esquiva Perfecta",
                description="Esquiva 5 ataques consecutivos",
                category="combat",
                requirement={"consecutive_dodges": 5},
                reward={"type": "exp", "amount": 200},
                progress_max=5
            ),
            "flawless_victory": Achievement(
                id="flawless_victory",
                name="Victoria Impecable",
                description="Completa un combate sin recibir daño",
                category="combat",
                requirement={"flawless_combat": 1},
                reward={"type": "gold", "amount": 200},
                progress_max=1
            ),
            "berserker": Achievement(
                id="berserker",
                name="Berserker",
                description="Derrota 5 enemigos con menos del 10% de vida",
                category="combat",
                requirement={"low_hp_kills": 5},
                reward={"type": "exp", "amount": 500},
                progress_max=5
            ),
            
            # Logros de progresión
            "level_10": Achievement(
                id="level_10",
                name="Ascenso",
                description="Alcanza el nivel 10",
                category="progression",
                requirement={"level": 10},
                reward={"type": "gold", "amount": 300},
                progress_max=10
            ),
            "level_25": Achievement(
                id="level_25",
                name="Héroe Veterano",
                description="Alcanza el nivel 25",
                category="progression",
                requirement={"level": 25},
                reward={"type": "gold", "amount": 1000},
                progress_max=25
            ),
            "level_50": Achievement(
                id="level_50",
                name="Leyenda Viviente",
                description="Alcanza el nivel 50",
                category="progression",
                requirement={"level": 50},
                reward={"type": "gold", "amount": 3000},
                progress_max=50
            ),
            "max_level": Achievement(
                id="max_level",
                name="Poder Absoluto",
                description="Alcanza el nivel máximo (70)",
                category="progression",
                requirement={"level": 70},
                reward={"type": "gold", "amount": 10000},
                progress_max=70
            ),
            
            # Logros de colección
            "weapon_collector": Achievement(
                id="weapon_collector",
                name="Coleccionista de Armas",
                description="Posee 5 armas diferentes",
                category="collection",
                requirement={"unique_weapons": 5},
                reward={"type": "gold", "amount": 500},
                progress_max=5
            ),
            "wealthy": Achievement(
                id="wealthy",
                name="Mercader Rico",
                description="Acumula 1000 de oro",
                category="collection",
                requirement={"gold": 1000},
                reward={"type": "exp", "amount": 300},
                progress_max=1000
            ),
            "millionaire": Achievement(
                id="millionaire",
                name="Millonario",
                description="Acumula 10000 de oro",
                category="collection",
                requirement={"gold": 10000},
                reward={"type": "exp", "amount": 2000},
                progress_max=10000,
                hidden=True
            ),
            
            # Logros especiales/secretos
            "survivor": Achievement(
                id="survivor",
                name="Superviviente",
                description="Sobrevive con 1 punto de vida",
                category="special",
                requirement={"survived_1hp": 1},
                reward={"type": "gold", "amount": 500},
                progress_max=1,
                hidden=True
            ),
            "shopaholic": Achievement(
                id="shopaholic",
                name="Adicto a las Compras",
                description="Visita la tienda 20 veces",
                category="special",
                requirement={"shop_visits": 20},
                reward={"type": "gold", "amount": 300},
                progress_max=20
            ),
            "dungeon_walker": Achievement(
                id="dungeon_walker",
                name="Caminante de Mazmorras",
                description="Camina 1000 pasos en las mazmorras",
                category="exploration",
                requirement={"steps_walked": 1000},
                reward={"type": "exp", "amount": 500},
                progress_max=1000
            ),
            "comeback_king": Achievement(
                id="comeback_king",
                name="Rey del Regreso",
                description="Gana un combate después de estar bajo 20% de vida 3 veces",
                category="combat",
                requirement={"comeback_wins": 3},
                reward={"type": "exp", "amount": 800},
                progress_max=3,
                hidden=True
            ),
            "speed_runner": Achievement(
                id="speed_runner",
                name="Velocista",
                description="Alcanza el nivel 30 en menos de 100 combates",
                category="special",
                requirement={"level_30_fast": 1},
                reward={"type": "gold", "amount": 2000},
                progress_max=1,
                hidden=True
            ),
            "state_master": Achievement(
                id="state_master",
                name="Maestro de Estados",
                description="Aplica 50 estados alterados a enemigos",
                category="combat",
                requirement={"states_applied": 50},
                reward={"type": "exp", "amount": 600},
                progress_max=50
            ),
        }
    
    def check_achievement(self, achievement_id: str, progress_data: Dict) -> bool:
        """
        Verifica si se cumple un logro y lo desbloquea.
        
        Args:
            achievement_id: ID del logro a verificar
            progress_data: Datos actuales del progreso del jugador
            
        Returns:
            True si el logro fue desbloqueado, False en caso contrario
        """
        if achievement_id not in self.achievements:
            return False
        
        achievement = self.achievements[achievement_id]
        
        # Si ya está desbloqueado, no hacer nada
        if achievement.unlocked:
            return False
        
        # Actualizar progreso
        for key, required_value in achievement.requirement.items():
            if key in progress_data:
                achievement.progress = min(progress_data[key], achievement.progress_max)
        
        # Verificar si se cumple el requisito
        requirement_met = all(
            progress_data.get(key, 0) >= value
            for key, value in achievement.requirement.items()
        )
        
        if requirement_met:
            achievement.unlocked = True
            achievement.unlock_date = datetime.now().isoformat()
            self.save_progress()
            return True
        
        return False
    
    def update_progress(self, progress_type: str, value: int):
        """
        Actualiza el progreso y verifica todos los logros relevantes.
        
        Args:
            progress_type: Tipo de progreso ("enemies_defeated", "level", etc.)
            value: Valor actual del progreso
            
        Returns:
            Lista de IDs de logros recién desbloqueados
        """
        newly_unlocked = []
        progress_data = {progress_type: value}
        
        for achievement_id, achievement in self.achievements.items():
            if not achievement.unlocked and progress_type in achievement.requirement:
                if self.check_achievement(achievement_id, progress_data):
                    newly_unlocked.append(achievement_id)
        
        return newly_unlocked
    
    def get_achievement(self, achievement_id: str) -> Optional[Achievement]:
        """Obtiene un logro específico."""
        return self.achievements.get(achievement_id)
    
    def get_all_achievements(self, include_hidden: bool = False) -> List[Achievement]:
        """Obtiene todos los logros."""
        if include_hidden:
            return list(self.achievements.values())
        return [a for a in self.achievements.values() if not a.hidden or a.unlocked]
    
    def get_unlocked_achievements(self) -> List[Achievement]:
        """Obtiene solo los logros desbloqueados."""
        return [a for a in self.achievements.values() if a.unlocked]
    
    def get_achievements_by_category(self, category: str) -> List[Achievement]:
        """Obtiene logros por categoría."""
        return [a for a in self.achievements.values() if a.category == category]
    
    def get_completion_percentage(self) -> float:
        """Calcula el porcentaje de logros completados."""
        total = len(self.achievements)
        unlocked = len(self.get_unlocked_achievements())
        return (unlocked / total * 100) if total > 0 else 0.0
    
    def get_category_completion(self) -> Dict[str, float]:
        """Calcula el porcentaje de completitud por categoría."""
        categories = {}
        for achievement in self.achievements.values():
            if achievement.category not in categories:
                categories[achievement.category] = {"total": 0, "unlocked": 0}
            categories[achievement.category]["total"] += 1
            if achievement.unlocked:
                categories[achievement.category]["unlocked"] += 1
        
        return {
            cat: (data["unlocked"] / data["total"] * 100) if data["total"] > 0 else 0.0
            for cat, data in categories.items()
        }
    
    def save_progress(self):
        """Guarda el progreso de logros en archivo JSON."""
        try:
            save_data = {
                achievement_id: {
                    "unlocked": achievement.unlocked,
                    "unlock_date": achievement.unlock_date,
                    "progress": achievement.progress
                }
                for achievement_id, achievement in self.achievements.items()
            }
            
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving achievements: {e}")
            return False
    
    def load_progress(self):
        """Carga el progreso de logros desde archivo JSON."""
        try:
            if not os.path.exists(self.save_file):
                return
            
            with open(self.save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            for achievement_id, data in save_data.items():
                if achievement_id in self.achievements:
                    self.achievements[achievement_id].unlocked = data.get("unlocked", False)
                    self.achievements[achievement_id].unlock_date = data.get("unlock_date")
                    self.achievements[achievement_id].progress = data.get("progress", 0)
            
        except Exception as e:
            print(f"Error loading achievements: {e}")
    
    def reset_all(self):
        """Resetea todos los logros (para testing)."""
        for achievement in self.achievements.values():
            achievement.unlocked = False
            achievement.unlock_date = None
            achievement.progress = 0
        self.save_progress()
    
    def to_dict(self) -> Dict:
        """Serializa el estado de achievements para guardado."""
        return {
            achievement_id: {
                "unlocked": achievement.unlocked,
                "unlock_date": achievement.unlock_date,
                "progress": achievement.progress
            }
            for achievement_id, achievement in self.achievements.items()
        }
    
    def from_dict(self, data: Dict):
        """Carga el estado de achievements desde un diccionario."""
        for achievement_id, achievement_data in data.items():
            if achievement_id in self.achievements:
                self.achievements[achievement_id].unlocked = achievement_data.get("unlocked", False)
                self.achievements[achievement_id].unlock_date = achievement_data.get("unlock_date")
                self.achievements[achievement_id].progress = achievement_data.get("progress", 0)


# Instancia global del gestor de logros
_achievement_manager = None


def get_achievement_manager() -> AchievementManager:
    """Obtiene la instancia global del AchievementManager."""
    global _achievement_manager
    if _achievement_manager is None:
        _achievement_manager = AchievementManager()
    return _achievement_manager
