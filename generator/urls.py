from django.conf.urls import url

from . import views

app_name = 'generator'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/generate/$', views.generate, name='generate'),
    url(r'^canvastest/$', views.canvastest, name='canvastest'),
]