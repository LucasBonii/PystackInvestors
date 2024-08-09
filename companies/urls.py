from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar_empresa/', views.register_company, name="register_company"),
    path('listar_empresas/', views.list_companies, name="list_companies"),
]
