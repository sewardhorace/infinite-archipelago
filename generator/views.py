from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from core.namer import Namer
from core.scrambler import Scrambler
from .models import Detail, Component, Game


#will remove the below file access stuff when the data is stored in the db
import os, json
from infinitelabyrinth.settings import BASE_DIR

input_data = {}
with open(os.path.join(BASE_DIR, 'core/input_data/data.json')) as json_data:
    input_data = json.load(json_data)
scrambler = Scrambler(input_data)

input_data = {}
with open(os.path.join(BASE_DIR, 'core/corpora/data.json')) as json_data:
   input_data = json.load(json_data)
namer = Namer(input_data)

endpoints = {}
with open(os.path.join(BASE_DIR, 'core/input_data/endpoints.json')) as json_data:
    endpoints = json.load(json_data)




def index(request):
    context = {
        'endpoints': endpoints
    }
    return render(request, 'generator/index.html', context)

class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context

class ComponentCreate(CreateView):
    model = Component
    fields = ['name']

class ComponentUpdate(UpdateView):
    model = Component
    fields = ['name']

class ComponentDelete(DeleteView):
    model = Component

class ComponentCreate(CreateView):
    model = Component
    fields = ['name']

def generate(request):
    format_text = request.GET.get('text')
    text = scrambler.scramble(format_text)
    text = namer.generate(text)
    data = {
        'detail':text
    }
    # data = serializers.serialize("json", data)
    return JsonResponse(data)

def map_data(request):
    game = list(Game.objects.filter(id=1).values())[0]
    components = list(Component.objects.filter(game=game["id"]).values())
    game["components"] = components
    for component in game["components"]:
        details = list(Detail.objects.filter(component=component["id"]).values())
        component["details"] = details
    response = dict(game=game)
    # response = dict(components=list(Component.objects.values()))
    return JsonResponse(response)

def canvas_test_dungeon(request):
    context = {}
    return render(request, 'generator/dungeontest.html', context)

def canvas_test_sea(request):
    context = {}
    return render(request, 'generator/seatest.html', context)