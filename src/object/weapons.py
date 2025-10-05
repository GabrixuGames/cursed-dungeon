import json

def load_weapons(weapons_db):
    with open(weapons_db, 'r', encoding='utf-8') as archivo:
        armas = json.load(archivo)
    return armas
