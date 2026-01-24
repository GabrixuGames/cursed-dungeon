"""
Sistema de habilidades especiales para Cursed Dungeon.
Permite a los jugadores usar habilidades únicas en combate.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import random


@dataclass
class Skill:
    """Representa una habilidad especial."""
    id: str
    name: str
    description: str
    mana_cost: int
    cooldown: int
    damage_multiplier: float
    effects: Dict
    level_required: int
    skill_type: str  # "attack", "defense", "support", "special"


class SkillManager:
    """Gestor del sistema de habilidades."""
    
    def __init__(self):
        self.skills_db = self._initialize_skills()
        self.cooldowns = {}  # {skill_id: turns_remaining}
        self.max_mana = 100
        self.current_mana = 100
        self.mana_regen_per_turn = 10
    
    def _initialize_skills(self) -> Dict[str, Skill]:
        """Inicializa la base de datos de habilidades."""
        return {
            # Habilidades de ataque
            "power_strike": Skill(
                id="power_strike",
                name="Golpe Poderoso",
                description="Un ataque devastador que causa 2x daño",
                mana_cost=15,
                cooldown=3,
                damage_multiplier=2.0,
                effects={},
                level_required=1,
                skill_type="attack"
            ),
            "critical_slash": Skill(
                id="critical_slash",
                name="Corte Crítico",
                description="Ataque con 50% de probabilidad de golpe crítico (3x daño)",
                mana_cost=20,
                cooldown=4,
                damage_multiplier=1.5,
                effects={"crit_chance": 0.5, "crit_multiplier": 3.0},
                level_required=5,
                skill_type="attack"
            ),
            "whirlwind": Skill(
                id="whirlwind",
                name="Torbellino",
                description="Ataque múltiple que ignora 50% de la evasión enemiga",
                mana_cost=25,
                cooldown=5,
                damage_multiplier=1.8,
                effects={"ignore_evade": 0.5},
                level_required=10,
                skill_type="attack"
            ),
            
            # Habilidades defensivas
            "iron_defense": Skill(
                id="iron_defense",
                name="Defensa Férrea",
                description="Reduce el daño recibido en un 50% durante 2 turnos",
                mana_cost=15,
                cooldown=5,
                damage_multiplier=0.0,
                effects={"defense_buff": 0.5, "duration": 2},
                level_required=3,
                skill_type="defense"
            ),
            "counter_stance": Skill(
                id="counter_stance",
                name="Postura de Contraataque",
                description="Devuelve 30% del daño recibido al atacante",
                mana_cost=20,
                cooldown=6,
                damage_multiplier=0.0,
                effects={"counter_damage": 0.3, "duration": 3},
                level_required=8,
                skill_type="defense"
            ),
            
            # Habilidades de soporte
            "second_wind": Skill(
                id="second_wind",
                name="Segundo Aliento",
                description="Recupera 25% de vida máxima",
                mana_cost=30,
                cooldown=8,
                damage_multiplier=0.0,
                effects={"heal_percent": 0.25},
                level_required=7,
                skill_type="support"
            ),
            "focus": Skill(
                id="focus",
                name="Concentración",
                description="Aumenta el daño en 30% durante 3 turnos",
                mana_cost=15,
                cooldown=5,
                damage_multiplier=0.0,
                effects={"damage_buff": 0.3, "duration": 3},
                level_required=4,
                skill_type="support"
            ),
            "meditation": Skill(
                id="meditation",
                name="Meditación",
                description="Recupera 50 de maná pero pierdes un turno",
                mana_cost=0,
                cooldown=4,
                damage_multiplier=0.0,
                effects={"mana_restore": 50, "skip_turn": True},
                level_required=6,
                skill_type="support"
            ),
            
            # Habilidades especiales (desbloqueo por nivel)
            "berserker_rage": Skill(
                id="berserker_rage",
                name="Furia Berserker",
                description="Sacrifica 20% de vida para atacar con 3x daño",
                mana_cost=25,
                cooldown=7,
                damage_multiplier=3.0,
                effects={"health_cost_percent": 0.2},
                level_required=15,
                skill_type="special"
            ),
            "life_steal": Skill(
                id="life_steal",
                name="Robo de Vida",
                description="Ataque que recupera 50% del daño causado como vida",
                mana_cost=30,
                cooldown=6,
                damage_multiplier=1.5,
                effects={"lifesteal": 0.5},
                level_required=12,
                skill_type="attack"
            ),
            "divine_shield": Skill(
                id="divine_shield",
                name="Escudo Divino",
                description="Inmunidad total al daño por 1 turno",
                mana_cost=40,
                cooldown=10,
                damage_multiplier=0.0,
                effects={"invulnerable": True, "duration": 1},
                level_required=20,
                skill_type="defense"
            ),
            "chaos_strike": Skill(
                id="chaos_strike",
                name="Golpe del Caos",
                description="Daño aleatorio entre 0.5x y 4x, puede aplicar estado aleatorio",
                mana_cost=20,
                cooldown=5,
                damage_multiplier=0.0,  # Se calcula dinámicamente
                effects={"random_damage": (0.5, 4.0), "random_state": True},
                level_required=18,
                skill_type="special"
            ),
        }
    
    def get_available_skills(self, player_level: int) -> List[Skill]:
        """Retorna las habilidades disponibles para el nivel del jugador."""
        return [
            skill for skill in self.skills_db.values()
            if skill.level_required <= player_level
        ]
    
    def can_use_skill(self, skill_id: str) -> tuple[bool, str]:
        """
        Verifica si se puede usar una habilidad.
        
        Returns:
            (can_use, reason): Tupla con booleano y mensaje explicativo
        """
        if skill_id not in self.skills_db:
            return False, "Habilidad desconocida"
        
        skill = self.skills_db[skill_id]
        
        # Verificar cooldown
        if skill_id in self.cooldowns and self.cooldowns[skill_id] > 0:
            return False, f"En recarga ({self.cooldowns[skill_id]} turnos)"
        
        # Verificar maná
        if self.current_mana < skill.mana_cost:
            return False, f"Maná insuficiente (requiere {skill.mana_cost})"
        
        return True, "Disponible"
    
    def use_skill(self, skill_id: str) -> bool:
        """
        Usa una habilidad (consume maná y activa cooldown).
        
        Returns:
            True si se usó correctamente, False en caso contrario
        """
        can_use, reason = self.can_use_skill(skill_id)
        if not can_use:
            return False
        
        skill = self.skills_db[skill_id]
        
        # Consumir maná
        self.current_mana -= skill.mana_cost
        
        # Activar cooldown
        self.cooldowns[skill_id] = skill.cooldown
        
        return True
    
    def calculate_skill_damage(self, skill_id: str, base_damage: int) -> int:
        """Calcula el daño de una habilidad basado en el daño base."""
        if skill_id not in self.skills_db:
            return base_damage
        
        skill = self.skills_db[skill_id]
        
        # Manejar habilidades con daño aleatorio
        if "random_damage" in skill.effects:
            min_mult, max_mult = skill.effects["random_damage"]
            multiplier = random.uniform(min_mult, max_mult)
            return int(base_damage * multiplier)
        
        # Manejar críticos
        if "crit_chance" in skill.effects:
            if random.random() < skill.effects["crit_chance"]:
                return int(base_damage * skill.damage_multiplier * skill.effects["crit_multiplier"])
        
        return int(base_damage * skill.damage_multiplier)
    
    def apply_skill_effects(self, skill_id: str, character, enemy=None):
        """
        Aplica los efectos especiales de una habilidad.
        
        Returns:
            Dict con información sobre los efectos aplicados
        """
        if skill_id not in self.skills_db:
            return {}
        
        skill = self.skills_db[skill_id]
        effects_applied = {}
        
        # Curación
        if "heal_percent" in skill.effects:
            heal_amount = int(character.getHealth() * skill.effects["heal_percent"] / (1 - skill.effects["heal_percent"]))
            character.setHealth(min(character.getHealth() + heal_amount, 150 + (character.getLevel() - 1) * 10))
            effects_applied["heal"] = heal_amount
        
        # Costo de vida
        if "health_cost_percent" in skill.effects:
            cost = int(character.getHealth() * skill.effects["health_cost_percent"])
            character.setHealth(character.getHealth() - cost)
            effects_applied["health_cost"] = cost
        
        # Robo de vida (se calcula después del daño)
        if "lifesteal" in skill.effects:
            effects_applied["lifesteal"] = skill.effects["lifesteal"]
        
        # Restaurar maná
        if "mana_restore" in skill.effects:
            self.current_mana = min(self.max_mana, self.current_mana + skill.effects["mana_restore"])
            effects_applied["mana_restored"] = skill.effects["mana_restore"]
        
        # Buffs/debuffs temporales (se manejan externamente)
        if "duration" in skill.effects:
            effects_applied["buff_duration"] = skill.effects["duration"]
            effects_applied["buff_type"] = skill.skill_type
        
        return effects_applied
    
    def update_cooldowns(self):
        """Reduce los cooldowns en 1 (llamar al final de cada turno)."""
        for skill_id in list(self.cooldowns.keys()):
            self.cooldowns[skill_id] -= 1
            if self.cooldowns[skill_id] <= 0:
                del self.cooldowns[skill_id]
    
    def regenerate_mana(self):
        """Regenera maná al final del turno."""
        self.current_mana = min(self.max_mana, self.current_mana + self.mana_regen_per_turn)
    
    def reset_mana(self):
        """Resetea el maná a su máximo (al inicio de combate)."""
        self.current_mana = self.max_mana
    
    def get_skill_info(self, skill_id: str) -> Optional[Skill]:
        """Obtiene información de una habilidad."""
        return self.skills_db.get(skill_id)
