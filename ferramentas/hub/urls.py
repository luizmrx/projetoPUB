from django.urls import path
from . import views

app_name = 'hub'

urlpatterns = [
    path('', views.hub_page, name='hub_page'),
    path('cadastro', views.cadastro, name="cadastro"),
    path("login", views.login, name='login'),
    path("logout", views.logout, name="logout"),
]