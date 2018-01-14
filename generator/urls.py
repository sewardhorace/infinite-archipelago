from django.conf.urls import url

from . import views

app_name = 'generator'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^signup/$', views.signup_view, name='signup'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),

    url(r'^api/game/(?P<game_id>[0-9]+)/$', views.game_load, name='game'),
    url(r'^api/game/create/$', views.game_create, name="game_create"),
    url(r'^api/game/update/$', views.game_update, name="game_update"),
    url(r'^api/components/create/$', views.components_create, name='components_create'),
    url(r'^api/components/update/$', views.components_update, name='components_update'),
    url(r'^api/components/delete/$', views.components_delete, name='components_delete'),
    url(r'^api/details/create/$', views.details_create, name='details_create'),
    url(r'^api/details/update/$', views.details_update, name='details_update'),
    url(r'^api/details/delete/$', views.details_delete, name='details_delete'),

    url(r'^api/generate/$', views.generate, name='generate'),
    url(r'^api/sync/$', views.sync_sheet, name='syncsheet'),
    url(r'^oauth2callback/$', views.oauth2_callback, name='oauth2callback'),
    url(r'^deletecreds/$', views.delete_creds, name='deletecreds'),#for debugging (TODO: remove in prod)
]