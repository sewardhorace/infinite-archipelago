from django.conf.urls import url

from . import views

app_name = 'generator'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/generate/$', views.generate, name='generate'),
    url(r'^api/game/$', views.game, name='game'),
    url(r'^api/components/create/$', views.components_create, name='components_create'),
    url(r'^api/components/update/$', views.components_update, name='components_update'),
    url(r'^api/components/delete/$', views.components_delete, name='components_delete'),
    url(r'^api/details/create/$', views.details_create, name='details_create'),
    url(r'^api/details/update/$', views.details_update, name='details_update'),
    url(r'^api/details/delete/$', views.details_delete, name='details_delete'),
    url(r'^canvastest/dungeon/$', views.canvas_test_dungeon, name='dungeontest'),
    url(r'^canvastest/sea/$', views.canvas_test_sea, name='seatest'),
]