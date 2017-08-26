from django.forms import ModelForm
from .models import Game, Component, Detail

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'scrambler_data', 'scrambler_endpoints']

class ComponentForm(ModelForm):
    class Meta:
        model = Component
        fields = ['name', 'game', 'x', 'y', 'isActive', 'category']

class DetailForm(ModelForm):
    class Meta:
        model = Detail
        fields = ['content', 'component']