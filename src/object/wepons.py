import json

def cargar_armas(weaponsDb):
    with open(weaponsDb, 'r', encoding='utf-8') as archivo:
        armas = json.load(archivo)
    return armas
