from django.shortcuts import render, redirect, get_object_or_404
from receitas.models import Receita
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def index(request):
    """ Renderiza a pagina inicial com as receitas """
    receitas = Receita.objects.order_by('-data_receita').filter(publicada = True)
    paginator = Paginator(receitas, 3)
    page = request.GET.get('page')
    receitas_por_paginas = paginator.get_page(page)


    dados = {
        'receitas' : receitas_por_paginas
    }
    return render( request ,'index.html', dados)



def receita(request, receita_id):
    """ Renderiza a pagina de detalhes de uma receita """
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_exibir = {
        'receita' : receita
    }
    return render(request, 'receitas/receita.html', receita_a_exibir)

def buscar(request):
    """ Realiza a busca por receitas e renderiza uma pagina com os resultados"""
    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        receitas = Receita.objects.order_by('-data_receita').filter(nome_receita__icontains=nome_a_buscar).filter( publicada = True)
        receita_a_exibir = {
            'receitas': receitas
        }

    return render(request, 'buscar.html', receita_a_exibir)

def criar_receita(request):
    """ Permite ao usuario criar uma nova receita e salva no BD"""
    if request.method == 'POST':
        nome_receita= request.POST['nome_receita']
        ingredientes= request.POST['ingredientes']
        modo_preparo= request.POST['modo_preparo']
        tempo_preparo= request.POST['tempo_preparo']
        rendimento= request.POST['rendimento']
        categoria= request.POST['categoria']
        foto_receita = request.FILES['foto_receita']
        print(nome_receita,ingredientes, modo_preparo, tempo_preparo, rendimento, categoria, foto_receita)
        user = get_object_or_404(User,pk= request.user.id)
        receita = Receita.objects.create( pessoa =user, nome_receita=  nome_receita, ingredientes= ingredientes, modo_preparo= modo_preparo,
                                          tempo_preparo = tempo_preparo, rendimento= rendimento, categoria=categoria, foto_receita = foto_receita )
        receita.save()
        return redirect('dashboard')
    return render(request, 'receitas/criar_receita.html')


def deletar_receita(request, receita_id):
    """ Permite ao usuario deletar uma receita """
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')

def editar_receita(request, receita_id):
    """ Permite ao usuario editar uma receita """
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_exibir = {
        'receita': receita
    }
    return render(request, 'receitas/editar_receita.html', receita_a_exibir)

def atualizar_receita(request):
    """ Apos a edicao de uma receita, realiza a atualizacao no BD"""
    if request.method=='POST':
        receita_id = request.POST['receita_id']
        receita= Receita.objects.get(pk= receita_id)
        receita.nome_receita= request.POST['nome_receita']
        receita.ingredientes= request.POST['ingredientes']
        receita.modo_preparo= request.POST['modo_preparo']
        receita.tempo_preparo= request.POST['tempo_preparo']
        receita.rendimento= request.POST['rendimento']
        receita.categoria= request.POST['categoria']
        if 'foto_receita' in request.FILES:
            receita.foto_receita = request.FILES['foto_receita']
        receita.save()
        return redirect('dashboard')

def campo_vazio(campo, nome_do_campo, request):
    """ Verifica se o campo é vazio e emite uma mensagem de alerta caso positivo """
    if campo.strip():
        return False
    else:
        messages.error(request, f'O campo {nome_do_campo} não pode ser em branco')
        return True