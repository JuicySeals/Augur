import yaml
import os

def load_cities():
    path = os.path.join(os.path.dirname(__file__), 'cities.yml')
    with open(path) as file:
        return yaml.safe_load(file)

CITIES = load_cities()
