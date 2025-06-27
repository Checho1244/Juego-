import os
import importlib

MAPS_PACKAGE = "assets.maps"
MAPS_PATH = os.path.join("assets", "maps")

def list_available_maps():
    maps = []
    for filename in os.listdir(MAPS_PATH):
        if filename.endswith(".py") and filename != "__init__.py":
            name = os.path.splitext(filename)[0]
            maps.append(name.capitalize())
    return maps

def load_map(map_name):
    module_name = f"{MAPS_PACKAGE}.{map_name.lower()}"
    try:
        module = importlib.import_module(module_name)
        return module.map_data
    except (ModuleNotFoundError, AttributeError):
        print(f"Error al cargar el mapa: {map_name}")
        return []