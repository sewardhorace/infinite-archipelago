import os, json, random

from django.shortcuts import render

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
    format_string = ('{Subject} is a {race} {char_detail_physical}.\n'
        '{Subject} {char_trait_attitude} and {char_trait_manner}.\n'
        '{Subject} {char_ability_competency} and also {char_ability_move}.\n'
        '{Subject} is {char_inventory}.')

    name = scrambler.scramble(namer.full_name_string())
    description = scrambler.scramble(format_string, random.choice(['m', 'f']))

    character = Character(char_name=name, char_description=description)
    context = {'character': character}
    return render(request, 'generator/index.html', context)