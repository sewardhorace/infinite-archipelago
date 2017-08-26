import json

from infinitelabyrinth import settings

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login

from .models import Game, Component, Detail, CredentialsModel
from .forms import GameForm, ComponentForm, DetailForm

from core.namer import Namer
from core.scrambler import Scrambler
from core.helpers import process_sheet_data



#will remove the below file access stuff when the data is stored in the db
import os, json
from infinitelabyrinth.settings import BASE_DIR

# input_data = {}
# with open(os.path.join(BASE_DIR, 'core/input_data/data.json')) as json_data:
#     input_data = json.load(json_data)
# scrambler = Scrambler(input_data)

# input_data = {}
# with open(os.path.join(BASE_DIR, 'core/corpora/data.json')) as json_data:
#    input_data = json.load(json_data)
# namer = Namer(input_data)

# endpoints = {}
# with open(os.path.join(BASE_DIR, 'core/input_data/endpoints.json')) as json_data:
#     endpoints = json.load(json_data)

#OAuth2 stuff
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.contrib import xsrfutil
import httplib2
from googleapiclient import discovery

#TODO: secret keys
flow = OAuth2WebServerFlow(client_id='1009808248889-jb68jsfvb2ml8b8ebjf9mp8311qunf1c.apps.googleusercontent.com',
                           client_secret='7txINyvGVGkAyk_cwL6iuWKa',
                           scope='https://www.googleapis.com/auth/spreadsheets.readonly',
                           redirect_uri='http://localhost:8000/oauth2callback')

def delete_creds(request):
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    storage.delete()
    print('CREDS DELETED')
    return HttpResponseRedirect("/")


def oauth2_callback(request):
    print('OAUTH2 CALLBACK')
    state = request.GET.dict()['state'].encode('UTF-8')
    if not xsrfutil.validate_token(settings.SECRET_KEY, state, request.user):
        return  HttpResponseBadRequest()
    credentials = flow.step2_exchange(request.GET.dict()['code'])
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credentials)
    return HttpResponseRedirect("/")

def index(request):
    if request.user.is_authenticated:
        print("user %s is authenticated" % (request.user.username))
    else:
        print("user is not authenticated")
        username = 'seawardhorses'
        password = 'kelso&abner'
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print('logged in %s' % (user.username))
        else:
            print('unable to authenticate user')

    game = Game.objects.filter(user_id=request.user.id).first()
    endpoints = None
    if game:
        endpoints = json.loads(game.scrambler_endpoints)
    context = {
        'endpoints': endpoints
    }
    print(context)
    return render(request, 'generator/index.html', context)

def sync_sheet(request):
    if request.user.is_authenticated:
        print("user %s is authenticated" % (request.user.username))
        result = None
        storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
        credentials = storage.get()
        if credentials is None or credentials.invalid == True:
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
            game = get_object_or_404(Game, id=1)
            game.scrambler_endpoints = json.dumps(data.pop('endpoints', None))
            game.scrambler_data = json.dumps(data)
            game.save()
            print('SYNC SUCCESSFUL')
            return HttpResponseRedirect("/")
    else:
        return HttpResponseBadRequest()

def generate(request):
    format_text = request.GET.get('text')
    text = None
    game = Game.objects.filter(user_id=request.user.id).first()
    if game:
        data = json.loads(game.scrambler_data)
        text = Scrambler(data['tables']).scramble(format_text)
        text = Namer(data['corpora']).generate(text)
    data = {
        'detail':text
    }
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