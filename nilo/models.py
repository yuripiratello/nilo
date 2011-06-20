from django.db import models
from django.contrib.auth.models import User

class FuncoesBiologicas(models.Model):
    descricao = models.TextField()

    def __unicode__(self):
        return self.descricao
        
class Nutriente(models.Model):
    nome = models.CharField(max_length=100)
    funcoesbiologicas = models.ManyToManyField(FuncoesBiologicas, verbose_name="Funcoes Biologicas")
    
    def __unicode__(self):
        return self.nome

class Ingrediente(models.Model):
    nome = models.CharField(max_length=100)
    nutriente = models.ManyToManyField(Nutriente)
    
    
    def __unicode__(self):
        return self.nome

class Receita(models.Model):
    TIPOS_RECEITA = (
        ('A','Almoco'),
        ('J','Jantar'),
        ('L','Lanche'),
        ('M','Matinal'),
    )
    
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    quantidadeDeCalorias = models.FloatField(verbose_name='Qtd. de Calorias')
    mododepreparo = models.TextField(verbose_name="Modo de Preparo")
    
    def __unicode__(self):
        return self.nome

class ItensReceita(models.Model):
    TIPOS_UNIDADES = (
        ('k','Kilo'),
        ('l','Litro'),
        ('u','Unidade'),
        ('x','Xicara'),
        ('s','Colher de Sopa'),
        ('c','Colher de Cafe'),
        ('h','Colher de Cha'),
    )
    
    receita = models.ForeignKey(Receita)
    ingrediente = models.ForeignKey(Ingrediente)
    quantidade = models.CharField(max_length=50)
    unidade = models.CharField(max_length=1, choices = TIPOS_UNIDADES)
    
    def __unicode__(self):
        return self.ingrediente.nome

class Cardapio(models.Model):
    nome = models.CharField(max_length=200)
    #receita = models.ManyToManyField(Receita)
    #usuario = models.ManyToManyField(User)
    
    def __unicode__(self):
        return self.nome


class CardapioReceita(models.Model):
    cardapio = models.ForeignKey(Cardapio)
    receita = models.ForeignKey(Receita)

class UsuarioCardapio(models.Model):
    cardapio = models.ForeignKey(Cardapio)
    usuario = models.ForeignKey(User)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Usuario - Cardapio"
        verbose_name_plural = "Usuario - Cardapio"