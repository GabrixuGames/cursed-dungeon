"""
Test suite básico para Cursed Dungeon.
Ejecuta validaciones en los sistemas principales.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Verifica que todos los módulos principales se importen correctamente."""
    print("Testing imports...")
    try:
        from src.object.main_character import MainCharacter
        from src.object.enemy import Enemy
        from src.object.weapons import load_weapons
        from src.save_manager import get_save_manager
        from src.skill_system import SkillManager
        from src.achievement_system import get_achievement_manager
        from config import DisplayConfig, Colors
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_character_creation():
    """Prueba la creación de personajes."""
    print("\nTesting character creation...")
    try:
        from src.object.main_character import MainCharacter
        
        char = MainCharacter("TestHero")
        assert char.name == "TestHero"
        assert char.level == 1
        assert char.health == 150
        assert char.damage == 10
        assert char.evade_chance == 5
        assert char.experience == 0
        assert char.money == 0
        
        print("✓ Character creation successful")
        return True
    except AssertionError as e:
        print(f"✗ Character creation failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_character_properties():
    """Prueba el sistema de properties."""
    print("\nTesting character properties...")
    try:
        from src.object.main_character import MainCharacter
        
        char = MainCharacter("TestHero")
        
        # Test property setters
        char.level = 10
        assert char.level == 10
        
        char.health = 200
        assert char.health == 200
        
        # Test health cannot be negative
        char.health = -10
        assert char.health == 0
        
        # Test legacy methods still work
        char.setLevel(15)
        assert char.getLevel() == 15
        
        print("✓ Character properties work correctly")
        return True
    except AssertionError as e:
        print(f"✗ Properties test failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_enemy_creation():
    """Prueba la creación de enemigos."""
    print("\nTesting enemy creation...")
    try:
        from src.object.enemy import Enemy
        
        enemy = Enemy(
            name="Test Goblin",
            health=50,
            damage=10,
            attack_rate=0.7,
            evade_chance=5,
            level_min=1,
            level_max=5,
            state=[]
        )
        
        assert enemy.name == "Test Goblin"
        assert enemy.health == 50
        assert enemy.damage == 10
        assert enemy.level_min == 1
        assert enemy.level_max == 5
        
        print("✓ Enemy creation successful")
        return True
    except AssertionError as e:
        print(f"✗ Enemy creation failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_save_manager():
    """Prueba el sistema de guardado múltiple."""
    print("\nTesting save manager...")
    try:
        from src.save_manager import get_save_manager
        
        save_mgr = get_save_manager()
        
        # Test save paths
        assert save_mgr.MAX_SLOTS == 3
        path1 = save_mgr.get_save_path(1)
        assert "save_slot_1.json" in path1
        
        # Test list all saves
        saves = save_mgr.list_all_saves()
        assert len(saves) == 3
        
        print("✓ Save manager works correctly")
        return True
    except AssertionError as e:
        print(f"✗ Save manager test failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_skill_system():
    """Prueba el sistema de habilidades."""
    print("\nTesting skill system...")
    try:
        from src.skill_system import SkillManager
        
        skill_mgr = SkillManager()
        
        # Test skill availability
        skills_lvl1 = skill_mgr.get_available_skills(1)
        assert len(skills_lvl1) > 0
        
        skills_lvl20 = skill_mgr.get_available_skills(20)
        assert len(skills_lvl20) > len(skills_lvl1)
        
        # Test mana system
        assert skill_mgr.current_mana == 100
        assert skill_mgr.max_mana == 100
        
        # Test using a skill
        can_use, reason = skill_mgr.can_use_skill("power_strike")
        assert can_use == True
        
        success = skill_mgr.use_skill("power_strike")
        assert success == True
        assert skill_mgr.current_mana < 100
        
        print("✓ Skill system works correctly")
        return True
    except AssertionError as e:
        print(f"✗ Skill system test failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_achievement_system():
    """Prueba el sistema de logros."""
    print("\nTesting achievement system...")
    try:
        from src.achievement_system import get_achievement_manager
        
        ach_mgr = get_achievement_manager()
        
        # Test achievement retrieval
        first_blood = ach_mgr.get_achievement("first_blood")
        assert first_blood is not None
        assert first_blood.name == "Primera Sangre"
        
        # Test categories
        combat_achievements = ach_mgr.get_achievements_by_category("combat")
        assert len(combat_achievements) > 0
        
        # Test completion percentage
        completion = ach_mgr.get_completion_percentage()
        assert 0 <= completion <= 100
        
        print("✓ Achievement system works correctly")
        return True
    except AssertionError as e:
        print(f"✗ Achievement system test failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_weapon_loading():
    """Prueba la carga de armas desde la base de datos."""
    print("\nTesting weapon loading...")
    try:
        from src.object.weapons import load_weapons
        from src.others import resource_path
        
        weapons = load_weapons(resource_path("src/db/weaponsDb.json"))
        assert len(weapons) > 0
        
        # Verify weapon structure
        first_weapon = weapons[0]
        assert "name" in first_weapon
        assert "damage" in first_weapon
        assert "attack_ratio" in first_weapon
        assert "price" in first_weapon
        
        print(f"✓ Loaded {len(weapons)} weapons successfully")
        return True
    except AssertionError as e:
        print(f"✗ Weapon loading failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_enemy_database():
    """Prueba la carga de enemigos desde la base de datos."""
    print("\nTesting enemy database...")
    try:
        from src.object.enemy import load_enemies
        from src.object.main_character import MainCharacter
        from src.others import resource_path
        
        # Create test character
        char = MainCharacter("TestHero")
        char.level = 5
        
        # Load enemies
        enemies = load_enemies(resource_path("src/db/enemyDb.json"), char)
        assert len(enemies) > 0
        
        # Verify enemy structure
        first_enemy = enemies[0]
        assert hasattr(first_enemy, 'name')
        assert hasattr(first_enemy, 'health')
        assert hasattr(first_enemy, 'damage')
        assert hasattr(first_enemy, 'attack_rate')
        
        print(f"✓ Loaded {len(enemies)} enemies successfully")
        return True
    except AssertionError as e:
        print(f"✗ Enemy database test failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_config():
    """Verifica que la configuración esté correctamente definida."""
    print("\nTesting configuration...")
    try:
        from config import DisplayConfig, Colors, MenuConfig, FontConfig
        
        # Test DisplayConfig
        assert DisplayConfig.WINDOW_WIDTH == 1280
        assert DisplayConfig.WINDOW_HEIGHT == 720
        assert DisplayConfig.FPS == 60
        
        # Test Colors
        assert Colors.BLACK == (0, 0, 0)
        assert Colors.WHITE == (255, 255, 255)
        
        # Test MenuConfig exists and has expected attributes
        assert hasattr(MenuConfig, 'GAME_MENU_WIDTH')
        assert hasattr(MenuConfig, 'OPTION_SPACING')
        
        print("✓ Configuration is valid")
        return True
    except AssertionError as e:
        print(f"✗ Configuration test failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def run_all_tests():
    """Ejecuta todos los tests y genera un reporte."""
    print("=" * 60)
    print("CURSED DUNGEON - TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_config,
        test_character_creation,
        test_character_properties,
        test_enemy_creation,
        test_weapon_loading,
        test_enemy_database,
        test_save_manager,
        test_skill_system,
        test_achievement_system,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(tests)} tests")
    print(f"Success rate: {(passed/len(tests)*100):.1f}%")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
