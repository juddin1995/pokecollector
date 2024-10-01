import random
import requests
from django.shortcuts import render
from django.http import HttpResponse


class Pokemon:
    def __init__(self, name, xp, type, abilities, image_url):
        self.name = name
        self.xp = xp
        self.type = type
        self.abilities = abilities
        self.image_url = image_url

def home(request):
  return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def index(request):
    def fetch_random_pokemon():
        random_index = random.randint(1, 150)
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{random_index}/')
        if response.status_code == 200:
            data = response.json()
            name = data['name'].capitalize()
            xp = data['base_experience']
            type = data['types'][0]['type']['name']
            abilities = ', '.join([ability['ability']['name'] for ability in data['abilities']])
            image_url = data['sprites']['other']['official-artwork']['front_default']
            return Pokemon(name, xp, type, abilities, image_url)
        else:
            return None

    random_pokemon = fetch_random_pokemon()
    return render(request, 'pokemon/index.html', {'pokemon': random_pokemon})
