from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from receitas.models import Receita

# Create your views here.


def cadastro(request):
    if request.method == 'POST':

        nome = request.POST ['nome']
        email= request.POST ['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']

        if campo_vazio(nome, 'nome', request):
            return redirect('cadastro')
        if campo_vazio(email, 'email', request):
            return redirect('cadastro')
        if campo_vazio(senha, 'senha', request):
            return redirect('cadastro')
        if campo_vazio(senha2, 'senha', request):
            return redirect('cadastro')

        if senha.strip() != senha2.strip():
            messages.error(request, "As senhas digitadas devem ser iguais")
            return redirect('cadastro')

        if usuario_ja_cadastrado(request, nome, email):
            return redirect('cadastro')

        user = User.objects.create_user(username= nome, email= email, password= senha )
        user.save()
        messages.success(request, 'Usuário criado com sucesso')
        return redirect('login')
    return render(request, 'cadastro.html')

def login(request):
    if request.method == 'POST':
        email= request.POST ['email']
        senha = request.POST['senha']

        if not email.strip():
            messages.error(request, "O email não pode ser em branco")
            return redirect('login')
        if not senha.strip() :
            messages.error(request, "A senha não pode ser em branco")
            return redirect('login')
        if User.objects.filter(email=email).exists():
            username= User.objects.filter(email=email).values_list('username', flat= True).get()
            user = auth.authenticate(request, username= username, password = senha)
            if user is not None:
                auth.login(request,user)
                messages.success(request, username+" logado com sucesso")
                return redirect('dashboard')
    return render( request ,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    if request.user.is_authenticated:
        receitas = None

        receitas = Receita.objects.order_by('-data_receita').filter(pessoa= request.user.id)
        if (not receitas.exists()):
            receitas = None
        receita_a_exibir = {
            'receitas': receitas
        }
        return render( request ,'dashboard.html', receita_a_exibir)
    return redirect('index')

def criar_receita(request):
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
    return render(request, 'criar_receita.html')

def campo_vazio(campo, nome_do_campo, request):
    if campo.strip():
        return False
    else:
        messages.error(request, f'O campo {nome_do_campo} não pode ser em branco')
        return True

def usuario_ja_cadastrado(request, nome, email):
    if User.objects.filter(email=email).exists():
        messages.error(request, "Usuário já cadastrado")
        return True
    if User.objects.filter(username=nome).exists():
        messages.error(request, "Nome de usuário já cadastrado")
        return True
    return False
