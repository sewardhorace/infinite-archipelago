import os, json, random

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers

from infinitelabyrinth.settings import BASE_DIR
from core.namer import CharacterNamer
from core.scrambler import Scrambler
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
        character = Character.generate(scrambler, namer)
        data = {
            'type': 'character',
            'character': {
                'char_name': character.char_name,
                'char_description': character.char_description
            }
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

def canvastest(request):
    context = {}
    return render(request, 'generator/canvastest.html', context)