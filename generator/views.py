import json

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from core.namer import Namer
from core.scrambler import Scrambler
from .models import Detail, Component, Game
from .forms import ComponentForm, DetailForm


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

def generate(request):
    format_text = request.GET.get('text')
    text = scrambler.scramble(format_text)
    text = namer.generate(text)
    data = {
        'detail':text
    }
    # data = serializers.serialize("json", data)
    return JsonResponse(data)

def game(request):
    game = list(Game.objects.filter(id=1).values())[0]
    components = list(Component.objects.filter(game=game["id"]).values())
    game["components"] = components
    for component in game["components"]:
        details = list(Detail.objects.filter(component=component["id"]).values())
        component["details"] = details
    response = dict(game=game)
    return JsonResponse(response)

def components_create(request):
    response = dict()
    if request.method == 'POST':
        component_data = json.loads(request.body.decode('utf-8'))
        form = ComponentForm(component_data)
        if form.is_valid():
            component = form.save()
            response['component'] = dict(list(Component.objects.filter(id=component.id).values())[0])
            return JsonResponse(response)
        else:
            # TODO
            print("suk it")
    return JsonResponse(response)

def components_update(request):
    response = dict()
    if request.method == 'POST':
        component_data = json.loads(request.body.decode('utf-8'))
        component = get_object_or_404(Component, id=int(component_data['id']))
        form = ComponentForm(component_data, instance=component)
        if form.is_valid():
            form.save()
            response['component'] = dict(list(Component.objects.filter(id=component.id).values())[0])
            return JsonResponse(response)
    return JsonResponse(response)

def components_delete(request):
    #TODO: return some response
    response = dict()
    if request.method == 'POST':
        component_data = json.loads(request.body.decode('utf-8'))
        component = get_object_or_404(Component, id=int(component_data['id']))
        component.delete()
        return JsonResponse(response)
    return JsonResponse(response)

def details_create(request):
    response = dict()
    if request.method == 'POST':
        detail_data = json.loads(request.body.decode('utf-8'))
        form = DetailForm(detail_data)
        if form.is_valid():
            detail = form.save()
            response['detail'] = dict(list(Detail.objects.filter(id=detail.id).values())[0])
            return JsonResponse(response)
        else:
            # TODO
            print("suk it")
    return JsonResponse(response)

def details_update(request):
    response = dict()
    if request.method == 'POST':
        detail_data = json.loads(request.body.decode('utf-8'))
        detail = get_object_or_404(Detail, id=int(detail_data['id']))
        form = DetailForm(detail_data, instance=detail)
        if form.is_valid():
            form.save()
            response['detail'] = dict(list(Detail.objects.filter(id=detail.id).values())[0])
            return JsonResponse(response)
    return JsonResponse(response)

def details_delete(request):
    #TODO: return some response
    response = dict()
    if request.method == 'POST':
        detail_data = json.loads(request.body.decode('utf-8'))
        detail = get_object_or_404(Detail, id=int(detail_data['id']))
        detail.delete()
        return JsonResponse(response)
    return JsonResponse(response)

def canvas_test_dungeon(request):
    context = {}
    return render(request, 'generator/dungeontest.html', context)

def canvas_test_sea(request):
    context = {
        'categories':Component.CATEGORY_CHOICES
    }
    return render(request, 'generator/seatest.html', context)