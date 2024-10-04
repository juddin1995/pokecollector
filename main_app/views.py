import random
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import Pokemon, Item
from .forms import PokemonNicknameForm, FeedingForm

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
            poke_id = data['id']
            xp = data['base_experience']
            poke_type = data['types'][0]['type']['name']
            abilities = ', '.join([ability['ability']['name'] for ability in data['abilities']])
            image_url = data['sprites']['other']['official-artwork']['front_default']
            return {
                'name': name,
                'poke_id': poke_id,
                'xp': xp,
                'type': poke_type,
                'abilities': abilities,
                'image_url': image_url
            }
        else:
            return None

    random_pokemon = fetch_random_pokemon()
    return render(request, 'pokemon/index.html', {'pokemon': random_pokemon})

def poke_detail(request, poke_id):
    try:
        pokemon = Pokemon.objects.get(poke_id=poke_id)
        feeding_form = FeedingForm()
        items_pokemon_doesnt_have = Item.objects.exclude(id__in=pokemon.items.all().values_list('id'))
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound("Pokemon not found")

    return render(request, 'pokemon/detail.html', {'pokemon': pokemon, 'feeding_form': feeding_form, 'items': items_pokemon_doesnt_have})

def catch_pokemon(request, poke_id):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{poke_id}/')
    
    if response.status_code == 200:
        data = response.json()
        name = data['name'].capitalize()
        poke_id = data['id']
        xp = data['base_experience']
        poke_type = data['types'][0]['type']['name']
        abilities = ', '.join([ability['ability']['name'] for ability in data['abilities']])
        image_url = data['sprites']['other']['official-artwork']['front_default']
        
        pokemon = Pokemon(
            name=name,
            poke_id=poke_id,
            xp=xp,
            type=poke_type,
            abilities=abilities,
            image_url=image_url
        )
        
        pokemon.save()

        return redirect('pokemon-index')
    else:
        return HttpResponse('Error fetching data from the Pokémon API')
    
def show_pokemon(request):
    pokemon = Pokemon.objects.all()
    return render(request, 'pokemon/show.html', {'pokemon': pokemon})

class PokemonDeleteView(DeleteView):
    model = Pokemon
    success_url = reverse_lazy('show-pokemon')

def update_nickname(request, poke_id):
    try:
        pokemon = Pokemon.objects.get(poke_id=poke_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound("Pokemon not found")

    if request.method == 'POST':
        form = PokemonNicknameForm(request.POST, instance=pokemon)
        if form.is_valid():
            form.save()
            return redirect('show-pokemon')
    else:
        form = PokemonNicknameForm(instance=pokemon)

    return render(request, 'pokemon/update_nickname.html', {'form': form, 'pokemon': pokemon})

def add_feeding(request, poke_id):
    try:
        pokemon = Pokemon.objects.get(poke_id=poke_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound("Pokemon not found")

    form = FeedingForm(request.POST)

    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.pokemon = pokemon
        new_feeding.save()
        return redirect('poke-detail', poke_id=poke_id)

    return render(request, 'pokemon/add_feeding.html', {'form': form, 'pokemon': pokemon})

class ItemCreate(CreateView):
    model = Item
    fields = '__all__'
    success_url = reverse_lazy('item-index')

class ItemList(ListView):
    model = Item

class ItemDetail(DetailView):
    model = Item

class ItemUpdate(UpdateView):
    model = Item
    fields = ['name', 'effect']

class ItemDelete(DeleteView):
    model = Item
    success_url = reverse_lazy('item-index')

def assoc_item(request, item_id, poke_id):
    Pokemon.objects.get(poke_id=poke_id).items.add(item_id)
    return redirect('poke-detail', poke_id=poke_id)

def remove_item(request, item_id, poke_id):
    Pokemon.objects.get(poke_id=poke_id).items.remove(item_id)
    return redirect('poke-detail', poke_id=poke_id)