import json
import os

def load_weapons(weapons_db):
    """Load weapons from JSON file with error handling."""
    try:
        # Check if file exists
        if not os.path.exists(weapons_db):
            raise FileNotFoundError(f"Weapons database not found: {weapons_db}")
        
        # Check if file is readable
        if not os.access(weapons_db, os.R_OK):
            raise PermissionError(f"Cannot read weapons database: {weapons_db}")
            
        with open(weapons_db, 'r', encoding='utf-8') as archivo:
            weapons = json.load(archivo)
            
        # Validate weapons data
        if not isinstance(weapons, list):
            raise ValueError("Weapons data should be a list")
            
        if not weapons:
            raise ValueError("Weapons database is empty")
            
        # Validate each weapon has required fields
        required_fields = ["name", "damage", "attack_ratio", "price"]
        for i, weapon in enumerate(weapons):
            if not isinstance(weapon, dict):
                raise ValueError(f"Weapon {i} is not a valid object")
            
            for field in required_fields:
                if field not in weapon:
                    raise KeyError(f"Weapon {i} missing required field: {field}")
                    
            # Validate data types
            if not isinstance(weapon["damage"], (int, float)) or weapon["damage"] <= 0:
                raise ValueError(f"Weapon {i} has invalid damage value")
            if not isinstance(weapon["attack_ratio"], (int, float)) or weapon["attack_ratio"] <= 0:
                raise ValueError(f"Weapon {i} has invalid attack_ratio value")
            if not isinstance(weapon["price"], (int, float)) or weapon["price"] < 0:
                raise ValueError(f"Weapon {i} has invalid price value")
                
        return weapons
        
    except FileNotFoundError as e:
        print(f"Weapons file not found: {e}")
        # Return default weapon as fallback
        return [{"name": "Basic Sword", "damage": 10, "attack_ratio": 1200, "price": 0}]
        
    except PermissionError as e:
        print(f"Permission error reading weapons: {e}")
        return [{"name": "Basic Sword", "damage": 10, "attack_ratio": 1200, "price": 0}]
        
    except json.JSONDecodeError as e:
        print(f"Error parsing weapons file (corrupted JSON): {e}")
        return [{"name": "Basic Sword", "damage": 10, "attack_ratio": 1200, "price": 0}]
        
    except (KeyError, ValueError) as e:
        print(f"Invalid weapons data: {e}")
        return [{"name": "Basic Sword", "damage": 10, "attack_ratio": 1200, "price": 0}]
        
    except Exception as e:
        print(f"Unexpected error loading weapons: {e}")
        return [{"name": "Basic Sword", "damage": 10, "attack_ratio": 1200, "price": 0}]
