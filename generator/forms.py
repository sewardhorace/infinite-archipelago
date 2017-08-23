from django.forms import ModelForm
from .models import Detail, Component, Game

class ComponentForm(ModelForm):
    class Meta:
        model = Component
        fields = ['name', 'game', 'x', 'y', 'isActive', 'category']

class DetailForm(ModelForm):
    class Meta:
        model = Detail
        fields = ['content', 'component']