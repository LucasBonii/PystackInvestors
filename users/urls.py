from django.urls import path
from . import views


urlpatterns = [
    path('cadastro/', views.register, name="register"),
    path('logar/', views.login, name="login"),
    path('logout/', views.logout_view, name="logout_view"),
]
