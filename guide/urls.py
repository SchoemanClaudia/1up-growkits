from django.urls import path
from . import views

urlpatterns = [
    path('', views.grow_guide, name='grow_guide'),
]
