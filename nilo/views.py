# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from nilo.models import *
from django.template import RequestContext
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def index(request):
    usuario = request.user
    cardapios = UsuarioCardapio.objects.filter(usuario = usuario)
    return render_to_response('listaCardapios.html', {'cardapios' : cardapios, 'user':usuario,})

@login_required
def visualizarReceitas(request,id):
    usuario = request.user
    car = Cardapio.objects.get(pk=id)
    carRec = CardapioReceita.objects.filter(cardapio=car)
    receitas = []
    for rec in carRec:
        rec.receita.tipo_full = []
        for t in rec.receita.tipo:
            for T in rec.receita.TIPOS_RECEITA:
                if t == T[0]:
                    rec.receita.tipo_full.append(T[1])
        receitas.append(rec.receita)
    return  render_to_response('receitas.html', {'receitas' : receitas, 'user':usuario, 'cardapio':car,}, context_instance=RequestContext(request))

@login_required
def alterarSenha(request):
    usuario = request.user
    if request.POST:
        form = PasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.save()
        else:
            pass
    else:
        form = PasswordChangeForm(user = usuario)
    return render_to_response('alterarSenha.html', {'form':form,'user':usuario}, context_instance=RequestContext(request))