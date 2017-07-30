import os, json, random

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers

from infinitelabyrinth.settings import BASE_DIR
from core.namer import CharacterNamer
from core.scrambler import Scrambler
from core.sector import Sector
from .models import Character, Room


input_data = {}
with open(os.path.join(BASE_DIR, 'core/input_data/data.json')) as json_data:
    input_data = json.load(json_data)

scrambler = Scrambler(input_data)

names_corpus = []
with open(os.path.join(BASE_DIR, 'core/corpora/char_names_3.txt')) as f:
    names_corpus = f.read().lower().split()

namer = CharacterNamer(names_corpus)


def index(request):
    character = Character.generate(scrambler, namer)
    room = Room.generate(scrambler)

    ship_format_string = ('The ship...\n'
        '- {ship_feature}.\n'
        '- {ship_construction}.\n'
        '- {ship_speed}.\n'
        '- {ship_handling}.')
    ship = scrambler.scramble(ship_format_string)
    crew_format_string = ('The crew...\n'
        '- {crew_appearance}.\n'
        '- {crew_story}.\n'
        '- {crew_method}.\n')
    crew = scrambler.scramble(crew_format_string)
    loot_format_string = '{item_misc}'
    loot = scrambler.scramble(loot_format_string)

    context = {
        'character': character,
        'ship': ship,
        'crew': crew,
        'room': room,
        'loot': loot,
    }
    return render(request, 'generator/index.html', context)

def generate(request):
    data = {}
    if request.GET.get('type') == 'character':
        character = Character.generate(scrambler, namer)
        data = {
            'type': 'character',
            'character': {
                'char_name': character.char_name,
                'char_description': character.char_description
            }
        }
    elif request.GET.get('type') == 'ship':
        ship_format_string = ('The ship...\n'
        '- {ship_feature}.\n'
        '- {ship_construction}.\n'
        '- {ship_speed}.\n'
        '- {ship_handling}.')
        ship = scrambler.scramble(ship_format_string)
        data = {
            'type': 'ship',
            'ship': ship
    }
    elif request.GET.get('type') == 'crew':
        crew_format_string = ('The crew...\n'
        '- {crew_appearance}.\n'
        '- {crew_story}.\n'
        '- {crew_method}.\n')
        crew = scrambler.scramble(crew_format_string)
        data = {
            'type': 'crew',
            'crew': crew
    }
    elif request.GET.get('type') == 'room':
        room = Room.generate(scrambler)
        data = {
            'type': 'room',
            'room': room.room_description
        }
    elif request.GET.get('type') == 'loot':
        loot_format_string = '{item_misc}'
        loot = scrambler.scramble(loot_format_string)
        data = {
            'type': 'loot',
            'loot': loot
        }
    # data = serializers.serialize("json", data)
    return JsonResponse(data)

def map_data(request):
    '''
    if a user clicks on a door that opens a cooridor that is on a sector border,
    pause to generate the next sector before revealing the corridor,
    and merge the corridor with the new one created in the new sector

    request.GET.get('sectorId')
    request.GET.get('sectorExitPoint') x,y cooridinates to discern which side 
    and which corridor
    '''
    room = Sector().rooms[0]
    #TODO: serializers
    data = {
            'rooms': [{
                'x': room.x,
                'y': room.y,
                'width': room.width,
                'height': room.height,
                'isActive': False
            }],
            'doors':[],
            'corridors':[]
        }
    return JsonResponse(data)

def canvastest(request):
    context = {}
    return render(request, 'generator/canvastest.html', context)