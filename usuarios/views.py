from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita
from receitas.views.receita import campo_vazio

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
    return render(request, 'usuarios/cadastro.html')

def login(request):
    if request.method == 'POST':
        email= request.POST ['email']
        senha = request.POST['senha']

        if campo_vazio(email, 'email', request):
            return redirect('login')
        if campo_vazio(senha, 'senha', request):
            return redirect('login')
        if User.objects.filter(email=email).exists():
            username= User.objects.filter(email=email).values_list('username', flat= True).get()
            user = auth.authenticate(request, username= username, password = senha)
            if user is not None:
                auth.login(request,user)
                messages.success(request, username+" logado com sucesso")
                return redirect('dashboard')
    return render( request ,'usuarios/login.html')

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
        return render( request ,'usuarios/dashboard.html', receita_a_exibir)
    return redirect('index')





def usuario_ja_cadastrado(request, nome, email):
    if User.objects.filter(email=email).exists():
        messages.error(request, "Usuário já cadastrado")
        return True
    if User.objects.filter(username=nome).exists():
        messages.error(request, "Nome de usuário já cadastrado")
        return True
    return False
