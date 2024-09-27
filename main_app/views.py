import requests
from django.shortcuts import render
from django.http import HttpResponse

class Pokemon:
    def __init__(self, name, type_, description, level):
        self.name = name
        self.type_ = type_
        self.description = description
        self.level = level
        self.sprite_url = None

    def get_sprite(self):
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{self.name.lower()}')
        if response.status_code == 200:
            data = response.json()
            self.sprite_url = data['sprites']['front_default']
        else:
            self.sprite_url = 'Sprite not found'

# Create a list of Pokemon instances
pokemon_list = [
    Pokemon('Pikachu', 'Electric', 'A friendly mouse-like Pokémon.', 15),
    Pokemon('Charizard', 'Fire/Flying', 'A powerful dragon with fiery breath.', 36),
    Pokemon('Bulbasaur', 'Grass/Poison', 'Has a plant bulb on its back that grows with it.', 12),
    Pokemon('Squirtle', 'Water', 'A small turtle that can shoot water from its mouth.', 10),
    Pokemon('Jigglypuff', 'Normal/Fairy', 'Sings soothing songs that can put people to sleep.', 8)
]

# Create your views here.
def home(request):
    return HttpResponse('<h1>Welcome to the Pokecollector App!</h1>')

def about(request):
    return render(request, 'about.html')

def pokemon_index(request):
    # Fetch sprite for each Pokemon
    for poke in pokemon_list:
        poke.get_sprite()
    
    return render(request, 'pokemon/index.html', {'pokemon_list': pokemon_list})
