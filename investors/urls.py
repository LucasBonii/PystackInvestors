from django.urls import path
from . import views


path('sugestao/', views.sugestions , name='sugestions')