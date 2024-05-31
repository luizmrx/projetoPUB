from django.urls import path
from . import views

urlpatterns = [
    path('', views.hub_page, name='hub_page'),
]