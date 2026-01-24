# 🛠️ DEVELOPMENT.md - Guía de Desarrollo

## 📋 Configuración del Entorno de Desarrollo

### 1. Requisitos Previos
- Python 3.9+
- Git
- Editor de código (VSCode recomendado)

### 2. Configuración Inicial

```bash
# Clonar repositorio
git clone [url-del-repo]
cd cursed-dungeon-main

# Configurar entorno virtual
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Estructura de Branches

```
main          → Código estable en producción
develop       → Desarrollo activo
feature/*     → Nuevas características
bugfix/*      → Corrección de bugs
hotfix/*      → Correcciones urgentes
```

---

## 🏗️ Arquitectura del Proyecto

### Principios de Diseño
- **Modularidad**: Cada sistema es independiente
- **Separación de responsabilidades**: Lógica, presentación y datos separados
- **Pythonic Code**: Uso de properties, type hints, docstrings
- **Error Handling**: Gestión robusta de errores con fallbacks

### Patrones Implementados
- **Singleton**: SaveManager, AchievementManager, SkillManager
- **Strategy**: Diferentes estrategias de ataque/defensa
- **Observer**: Sistema de logros observa eventos del juego
- **State**: Estados alterados del personaje y enemigos

---

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
python tests/test_suite.py

# Con verbose
python tests/test_suite.py -v
```

### Crear Nuevos Tests

```python
def test_nueva_funcionalidad():
    """Descripción del test."""
    print("\nTesting nueva funcionalidad...")
    try:
        # Setup
        objeto = ClaseATestear()
        
        # Test
        resultado = objeto.metodo()
        assert resultado == esperado
        
        print("✓ Test pasado")
        return True
    except AssertionError as e:
        print(f"✗ Test fallido: {e}")
        return False
```

---

## 📝 Estándares de Código

### Nomenclatura

```python
# Clases: PascalCase
class MainCharacter:
    pass

# Funciones y métodos: snake_case
def calculate_damage():
    pass

# Constantes: UPPER_SNAKE_CASE
MAX_HEALTH = 100

# Variables: snake_case
player_health = 150
```

### Documentación

```python
def function_name(param1: int, param2: str) -> bool:
    """
    Breve descripción de la función.
    
    Args:
        param1: Descripción del parámetro 1
        param2: Descripción del parámetro 2
    
    Returns:
        Descripción del valor retornado
    
    Raises:
        ValueError: Cuando ocurre X condición
    """
    pass
```

### Type Hints

```python
from typing import Dict, List, Optional, Tuple

def get_enemies(level: int) -> List[Enemy]:
    pass

def save_game(slot: int = 1) -> bool:
    pass

def load_data() -> Optional[Dict]:
    pass
```

---

## 🔧 Sistemas Principales

### 1. SaveManager (`src/save_manager.py`)

```python
from src.save_manager import get_save_manager

# Obtener instancia
save_mgr = get_save_manager()

# Guardar en slot
character_data = {...}
save_mgr.save_game(slot=1, character_data)

# Cargar desde slot
data = save_mgr.load_game(slot=1)

# Listar saves
saves = save_mgr.list_all_saves()
```

### 2. SkillManager (`src/skill_system.py`)

```python
from src.skill_system import SkillManager

# Crear manager
skill_mgr = SkillManager()

# Obtener habilidades disponibles
skills = skill_mgr.get_available_skills(player_level=10)

# Verificar si se puede usar
can_use, reason = skill_mgr.can_use_skill("power_strike")

# Usar habilidad
if can_use:
    skill_mgr.use_skill("power_strike")
    damage = skill_mgr.calculate_skill_damage("power_strike", base_damage)
```

### 3. AchievementManager (`src/achievement_system.py`)

```python
from src.achievement_system import get_achievement_manager

# Obtener instancia
ach_mgr = get_achievement_manager()

# Actualizar progreso
unlocked = ach_mgr.update_progress("enemies_defeated", 10)

# Obtener logros
all_achievements = ach_mgr.get_all_achievements()
unlocked_only = ach_mgr.get_unlocked_achievements()

# Estadísticas
completion = ach_mgr.get_completion_percentage()
by_category = ach_mgr.get_category_completion()
```

---

## 🎮 Integración de Nuevas Características

### Añadir Nueva Habilidad

1. Editar `src/skill_system.py`
2. Añadir en `_initialize_skills()`:

```python
"nueva_skill": Skill(
    id="nueva_skill",
    name="Nombre Mostrado",
    description="Descripción detallada",
    mana_cost=20,
    cooldown=5,
    damage_multiplier=1.5,
    effects={"buff_type": value},
    level_required=10,
    skill_type="attack"
)
```

### Añadir Nuevo Logro

1. Editar `src/achievement_system.py`
2. Añadir en `_initialize_achievements()`:

```python
"nuevo_logro": Achievement(
    id="nuevo_logro",
    name="Nombre del Logro",
    description="Descripción del logro",
    category="combat",
    requirement={"stat_name": value},
    reward={"type": "gold", "amount": 100},
    progress_max=value
)
```

### Añadir Nuevo Enemigo

1. Editar `src/db/enemyDb.json`
2. Añadir entrada en array "normal":

```json
{
  "name": "Nuevo Enemigo",
  "health": 50,
  "damage": 15,
  "attackRate": 0.75,
  "evadeChance": 5,
  "level_min": 10,
  "level_max": 15,
  "states": [
    {
      "state": "Envenenado",
      "chance": 30,
      "duration": 3,
      "effect": {"health": -4}
    }
  ]
}
```

---

## 🐛 Debugging

### Logs y Mensajes

```python
# Para debugging temporal
print(f"DEBUG: variable = {variable}")

# Para errores manejados
try:
    # código
except Exception as e:
    print(f"Error en función_x: {e}")
```

### Verificar Integridad

```bash
# Ejecutar tests
python tests/test_suite.py

# Verificar imports
python -c "from src.object.main_character import MainCharacter; print('OK')"

# Verificar pygame
python -c "import pygame; pygame.init(); print(pygame.version.ver)"
```

---

## 📊 Performance

### Optimización de Game Loop

```python
# Usar clock para controlar FPS
clock = pygame.time.Clock()
while running:
    # ... game logic
    clock.tick(60)  # 60 FPS
```

### Caché de Recursos

```python
# Precalcular frames de animación
frames = precalculate_bonfire_frames(font, size)

# Reutilizar surfaces
surface_cache = {}
```

---

## 🚀 Deployment

### Crear Ejecutable (PyInstaller)

```bash
# Instalar PyInstaller
pip install pyinstaller

# Crear ejecutable
pyinstaller --onefile --windowed --name="CursedDungeon" main.py

# El ejecutable estará en dist/
```

### Release Checklist

- [ ] Tests pasando (100%)
- [ ] Código refactorizado
- [ ] Documentación actualizada
- [ ] CHANGELOG.md actualizado
- [ ] Version bump en README
- [ ] Git tag creado
- [ ] Ejecutable testeado

---

## 📚 Recursos Útiles

### Documentación
- [Pygame Docs](https://www.pygame.org/docs/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Python Docstrings](https://www.python.org/dev/peps/pep-0257/)

### Herramientas
- **Black**: Formatter de código Python
- **Pylint**: Linter para Python
- **MyPy**: Type checker estático

---

## 🤝 Contribuir

### Flujo de Trabajo

1. Fork del repositorio
2. Crear branch (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -m 'Add: nueva caracteristica'`)
4. Push a branch (`git push origin feature/nueva-caracteristica`)
5. Crear Pull Request

### Convenciones de Commits

```
Add: Nueva característica
Fix: Corrección de bug
Refactor: Refactorización de código
Docs: Cambios en documentación
Test: Añadir o modificar tests
Style: Cambios de formato (sin afectar lógica)
```

---

## 📞 Contacto y Soporte

Para preguntas o problemas, consultar:
- Issues en GitHub
- Documentación en `/docs`
- AGENTS.md para estructura del equipo
- WORKFLOW.md para flujo de desarrollo

---

**Última actualización**: Enero 2026 - v0.4
