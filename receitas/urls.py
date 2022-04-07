from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name = 'index'),
    path('<int:receita_id>',receita, name = 'receita'),
    path('buscar', buscar, name = 'buscar'),
    path('criar_receita', criar_receita, name= 'criar_receita'),
    path('deletar_receita/<int:receita_id>', deletar_receita, name='deletar_receita'),
    path('editar_receita/<int:receita_id>', editar_receita, name='editar_receita'),
    path('atualizar_receita', atualizar_receita, name='atualizar_receita'),
]