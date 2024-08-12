from django.urls import path
from . import views

urlpatterns = [
    path('sugestao/', views.sugestions , name='sugestions'),
    path('ver_empresa/<int:id>', views.inspect_company , name='inspect_company'),
    path('realizar_proposta/<int:id>', views.make_proposal , name='make_proposal'),
    path('assinar_contrato/<int:id>', views.sign_contract, name="sign_contract"),
    path('gerenciar_propostas/<int:id>', views.manage_proposals, name="manage_proposals"),
]