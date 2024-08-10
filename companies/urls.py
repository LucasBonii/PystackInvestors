from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar_empresa/', views.register_company, name="register_company"),
    path('listar_empresas/', views.list_companies, name="list_companies"),
    path('detalhes/<int:id>', views.company_details, name="company_details"),
    path('add_doc/<int:id>', views.add_doc, name="add_doc"),
    path('delete_doc/<int:id>', views.delete_doc, name="delete_doc"),
    path('add_metric/<int:id>', views.add_metric, name="add_metric"),
]
