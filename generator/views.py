#TODO: 'require authenticated user' decorators

import json

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from infinitelabyrinth import settings

from .models import Game, Component, Detail, CredentialsModel
from .forms import GameForm, ComponentForm, DetailForm

from core.namer import Namer
from core.scrambler import Scrambler
from core.helpers import process_sheet_data, parse_sheet_url

#Google OAuth2
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.contrib import xsrfutil
import httplib2
from googleapiclient import discovery

flow = OAuth2WebServerFlow(client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
                           client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
                           scope='https://www.googleapis.com/auth/spreadsheets.readonly')
default_game_id = 3

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
    # game = Game.objects.get(id=default_game_id)
    game = Game.objects.all().first()
    context = {
        'endpoints': json.loads(game.scrambler_endpoints),
        'game_id': game.id,
        'categories':Component.CATEGORY_CHOICES,
    }
    return render(request, 'generator/welcome.html', context)

def signup_view(request):
    #TODO: validate password, username length
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username, password=password)
        user.save()
        print('Successfully created user %s' % user.username)
        login(request, user)
        return HttpResponseRedirect("/")
    else:
        return HttpResponseBadRequest()

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

def game_create(request):
    #TODO: does this need to be more flexible? (ex. creating game with name, scrambler data)
    #TODO: load newly created game on the frontend
    response = dict()
    if request.method == 'POST':
        game = Game.objects.create(user_id=request.user.id)
        game.save()
        response['game'] = dict(Game.objects.filter(id=game.id).values()[0])
        return JsonResponse(response)
    else:
        #TODO
        return JsonResponse(response)

def game_update(request):
    response = dict()
    if request.method == 'POST':
        game_data = json.loads(request.body.decode('utf-8'))
        game = get_object_or_404(Game, id=int(game_data['id']))
        form = GameForm(game_data, instance=game)
        if form.is_valid():
            form.save()
            response['game'] = dict(Game.objects.filter(id=game.id).values()[0])
            return JsonResponse(response)
        else:
            #TODO
            print(form.errors)
            print('invalid form')
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
            print(form.errors)
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
        game = Game.objects.get(id=game_id)
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
    # possible error: oauth credentials can expire (?) but this will still try to use the old creds
    # TODO: loading spinner on the frontend while processing
    # TODO: ensure game id is provided; if no URL provided, fall back to last URL used
    if request.user.is_authenticated and request.method == 'POST':
        game_id = request.POST.get("game-id")
        game = get_object_or_404(Game, id=game_id)
        sheet_url = request.POST.get("sheet-url") or game.sheet_url
        result = None
        storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
        credentials = storage.get()
        if credentials is None or credentials.invalid == True:
            flow.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
            flow.redirect_uri = '%s%s' % (request.META['HTTP_REFERER'],'oauth2callback')
            auth_uri = flow.step1_get_authorize_url()
            return HttpResponseRedirect(auth_uri)
        else:
            # google sheets API
            http = httplib2.Http()
            http = credentials.authorize(http)
            discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                            'version=v4')
            service = discovery.build('sheets', 'v4', http=http,
                                      discoveryServiceUrl=discoveryUrl)
            spreadsheetId = None
            #TODO: cleaner error handling/fallback
            if sheet_url:
                spreadsheetId = parse_sheet_url(sheet_url)
            else:
                return HttpResponseBadRequest()
            # return a spreadsheet collection
            result = service.spreadsheets().get(spreadsheetId=spreadsheetId, includeGridData=True).execute()
            data = process_sheet_data(result)
            game.scrambler_endpoints = json.dumps(data.pop('endpoints', None))
            game.scrambler_data = json.dumps(data)
            game.sheet_url = sheet_url
            game.save()
            return HttpResponseRedirect("/")
    else:
        return HttpResponseBadRequest()

def oauth2_callback(request):
    state = request.GET.dict()['state'].encode('UTF-8')
    if not xsrfutil.validate_token(settings.SECRET_KEY, state, request.user):
        return  HttpResponseBadRequest()
    flow.redirect_uri = '%s%s' % (request.META['HTTP_REFERER'],'oauth2callback')
    credentials = flow.step2_exchange(request.GET.dict()['code'])
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credentials)
    # TODO: need to somehow call the sync_sheet view again but need the user and game_id
    return HttpResponseRedirect("/")

def delete_creds(request):
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    storage.delete()
    return HttpResponseRedirect("/")