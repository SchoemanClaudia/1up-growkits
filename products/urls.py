from django.urls import path
from . import views

urlpatterns = [
    path('', views.mushroom_kits, name='products')
]