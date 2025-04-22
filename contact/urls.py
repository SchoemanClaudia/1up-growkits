from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_view, name='contact'),
    path('sent/', views.message_sent, name='message_sent'),
]
