import os, json, random

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers

from infinitelabyrinth.settings import BASE_DIR
from core.namer import CharacterNamer
from core.scrambler import Scrambler
from .models import Character


input_data = {}
with open(os.path.join(BASE_DIR, 'core/input_data/data.json')) as json_data:
    input_data = json.load(json_data)

scrambler = Scrambler(input_data)

names_corpus = []
with open(os.path.join(BASE_DIR, 'core/corpora/char_names_3.txt')) as f:
    names_corpus = f.read().lower().split()

namer = CharacterNamer(names_corpus)


def index(request):
    char_format_string = ('- {race} {char_detail_physical}.\n'
        '- {subject} {char_trait_attitude}.\n'
        '- {subject} {char_trait_manner}.\n'
        '- {subject} {char_ability_competency}.\n'
        '- {subject} {char_ability_move}.\n'
        '- {subject} is {char_inventory}.')

    char_name = scrambler.scramble(namer.full_name_string())
    char_description = scrambler.scramble(char_format_string, random.choice(['m', 'f']))
    character = Character(char_name=char_name, char_description=char_description)

    room_format_string = ('- the room is 25ft x 25ft.\n'
        '- {construction}.\n'
        '- {atmosphere}.\n'
        '- {feature}.')
    room_description = scrambler.scramble(room_format_string)
    room = room_description

    loot_format_string = '{item_misc}'
    loot = scrambler.scramble(loot_format_string)

    context = {
        'character': character,
        'room': room,
        'loot': loot,
    }
    return render(request, 'generator/index.html', context)

def generate(request):
    data = {}
    if request.GET.get('type') == 'character':
        char_format_string = ('- {race} {char_detail_physical}.\n'
            '- {subject} {char_trait_attitude}.\n'
            '- {subject} {char_trait_manner}.\n'
            '- {subject} {char_ability_competency}.\n'
            '- {subject} {char_ability_move}.\n'
            '- {subject} is {char_inventory}.')

        char_name = scrambler.scramble(namer.full_name_string())
        char_description = scrambler.scramble(char_format_string, random.choice(['m', 'f']))
        data = {
            'type': 'character',
            'character': {
                'char_name':char_name,
                'char_description': char_description
            }
        }
    elif request.GET.get('type') == 'room':
        room_format_string = ('- the room is 25ft x 25ft.\n'
        '- {construction}.\n'
        '- {atmosphere}.\n'
        '- {feature}.')
        room_description = scrambler.scramble(room_format_string)
        data = {
            'type': 'room',
            'room': room_description
        }
    elif request.GET.get('type') == 'loot':
        loot_format_string = '{item_misc}'
        loot_description = scrambler.scramble(loot_format_string)
        data = {
            'type': 'loot',
            'loot': loot_description
        }
    # data = serializers.serialize("json", data)
    return JsonResponse(data)
