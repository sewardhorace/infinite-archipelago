from django.conf.urls import url

from . import views

app_name = 'generator'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/generate/$', views.generate, name='generate'),
    url(r'^ajax/map_data/$', views.map_data, name='map_data'),
    url(r'^canvastest/dungeon/$', views.canvas_test_dungeon, name='dungeontest'),
    url(r'^canvastest/sea/$', views.canvas_test_sea, name='seatest'),
    

    url(r'^about/$', views.ComponentCreate.as_view()) #example; not currently usable
]