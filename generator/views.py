#TODO: 'require authenticated user' decorators

import json

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout

from infinitelabyrinth import settings

from .models import Game, Component, Detail, CredentialsModel
from .forms import GameForm, ComponentForm, DetailForm

from core.namer import Namer
from core.scrambler import Scrambler
from core.helpers import process_sheet_data

#Google OAuth2
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.contrib import xsrfutil
import httplib2
from googleapiclient import discovery

#TODO: secure secret keys
flow = OAuth2WebServerFlow(client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
                           client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
                           scope='https://www.googleapis.com/auth/spreadsheets.readonly',
                           redirect_uri='http://localhost:8000/oauth2callback')

default_game = Game.objects.get(id=3)
# default_game = None

def index(request):
    if request.user.is_authenticated:
        print("user %s is authenticated" % (request.user.username))
        return user_page(request)
    else:
        print("user is not authenticated")
        return welcome(request)

def user_page(request):
    #TODO: should return last edited game
    game = Game.objects.filter(user_id=request.user.id).first()
    if not game:
        game = Game.objects.create(user_id=request.user.id, scrambler_endpoints="{}", scrambler_data="{}")
    context = {
        'game_id': game.id,
        'categories':Component.CATEGORY_CHOICES,
    }
    return render(request, 'generator/index.html', context)

def welcome(request):
    game = default_game
    context = {
        'endpoints': json.loads(game.scrambler_endpoints),
        'game_id': game.id,
        'categories':Component.CATEGORY_CHOICES,
    }
    return render(request, 'generator/welcome.html', context)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            # TODO: Return an 'invalid login' error message.
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

def game_load(request, game_id):
    game = Game.objects.filter(id=game_id).values()[0]
    game.pop("scrambler_data")
    endpoints = dict(json.loads(game.pop("scrambler_endpoints")))
    game["endpoints"] = endpoints
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
            response['component'] = dict(Component.objects.filter(id=component.id).values()[0])
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
            response['component'] = dict(Component.objects.filter(id=component.id).values()[0])
            return JsonResponse(response)
    return JsonResponse(response)

def components_delete(request):
    #TODO: return some responseS
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
            response['detail'] = dict(Detail.objects.filter(id=detail.id).values()[0])
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
            response['detail'] = dict(Detail.objects.filter(id=detail.id).values()[0])
            return JsonResponse(response)
    return JsonResponse(response)

def details_delete(request):
    response = dict()
    if request.method == 'POST':
        detail_data = json.loads(request.body.decode('utf-8'))
        detail = get_object_or_404(Detail, id=int(detail_data['id']))
        detail.delete()
        return JsonResponse(response)
    return JsonResponse(response)

def generate(request):
    # TODO: cleanup
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        format_text = data.get('text', '')
        game_id = data.get('game_id')
        text = None
        game = Game.objects.filter(user_id=request.user.id).first()
        if game:
            data = json.loads(game.scrambler_data)
            text = Scrambler(data['tables']).scramble(format_text)
            text = Namer(data['corpora']).generate(text)
        else:
            game = Game.objects.filter(id=1).first()
            data = json.loads(game.scrambler_data)
            text = Scrambler(data['tables']).scramble(format_text)
            text = Namer(data['corpora']).generate(text)
        data = {
            'detail':text
        }
        return JsonResponse(data)
    else:
        message = "Something went wrong"
        return JsonResponse({'status':'false','message':message}, status=500)

def sync_sheet(request):
    # TODO: loading spinner on the frontend while processing
    if request.user.is_authenticated:
        print("user %s is authenticated" % (request.user.username))
        result = None
        storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
        credentials = storage.get()
        if credentials is None or credentials.invalid == True:
            print('verifying credentials...')
            flow.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
            auth_uri = flow.step1_get_authorize_url()
            return HttpResponseRedirect(auth_uri)
        else:
            print('credentials are solid, dude')
            http = httplib2.Http()
            http = credentials.authorize(http)
            discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                            'version=v4')
            service = discovery.build('sheets', 'v4', http=http,
                                      discoveryServiceUrl=discoveryUrl)
            #TODO: will have to parse the spreadsheet ID from url submitted by user?
            spreadsheetId = '1m1spaKGgfcQ1PSRQ6tZTSHL1lighQyQFVSKT-VyyM6A'
            #return a spreadsheet collection
            result = service.spreadsheets().get(spreadsheetId=spreadsheetId, includeGridData=True).execute()
            data = process_sheet_data(result)
            game = get_object_or_404(Game, id=default_game.id)
            game.scrambler_endpoints = json.dumps(data.pop('endpoints', None))
            game.scrambler_data = json.dumps(data)
            game.save()
            print('Successfully synced sheet with game %d' % (game.id))
            print(game.name)
            return HttpResponseRedirect("/")
    else:
        return HttpResponseBadRequest()

def oauth2_callback(request):
    state = request.GET.dict()['state'].encode('UTF-8')
    if not xsrfutil.validate_token(settings.SECRET_KEY, state, request.user):
        return  HttpResponseBadRequest()
    credentials = flow.step2_exchange(request.GET.dict()['code'])
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credentials)
    return HttpResponseRedirect("/")

def delete_creds(request):
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    storage.delete()
    return HttpResponseRedirect("/")