from nilo.models import Nutriente, Ingrediente, Receita, FuncoesBiologicas, ItensReceita, Cardapio, User, UsuarioCardapio, CardapioReceita
from django.contrib import admin
from django import forms

class NutrienteAdmin(admin.ModelAdmin):
    search_fields = ('nome', 'funcoesbiologicas__descricao')
    
class IngredienteAdmin(admin.ModelAdmin):
    search_fields = ('nutriente__nome','nome','nutriente__funcoesbiologicas__descricao')

class ItensReceitaInLine(admin.TabularInline):
    model = ItensReceita
    extra = 1
    raw_id_fields = ("ingrediente",)


class ReceitaForm(forms.ModelForm):
    TIPOS_RECEITA = (
        ('A','Almoco'),
        ('J','Jantar'),
        ('L','Lanche'),
        ('M','Matinal'),
    )
    tipo = forms.MultipleChoiceField(choices=TIPOS_RECEITA, widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = Receita

class ReceitaAdmin(admin.ModelAdmin):
    form = ReceitaForm
    inlines = [ItensReceitaInLine,]
    search_fields = ('nome', 'itensreceita__ingrediente__nutriente__funcoesbiologicas__descricao','itensreceita__ingrediente__nutriente__nome','itensreceita__ingrediente__nome')
    list_display = ('nome',)
    
class ReceitaInLine(admin.TabularInline):
    model = Receita
    extra = 1
    
class CardapioReceitaInLine(admin.TabularInline):
    model = CardapioReceita
    extra = 1
    raw_id_fields = ['receita',]
    
class CardapioAdmin(admin.ModelAdmin):
    inlines = [CardapioReceitaInLine,]
    
class UsuarioCardapioInLine(admin.TabularInline):
    model = UsuarioCardapio
    extra = 1

from django.db import transaction
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.html import escape
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect

csrf_protect_m = method_decorator(csrf_protect)

class UserAdmin(admin.ModelAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',)}),
        #(_('Important dates'), {'fields': ('date_joined')}),
        (_('Groups'), {'fields': ('groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )
    inlines = [UsuarioCardapioInLine,]
    exclude = ('last_login', 'date_joined','user_permissions',)
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('user_permissions',)

    def __call__(self, request, url):
        # this should not be here, but must be due to the way __call__ routes
        # in ModelAdmin.
        if url is None:
            return self.changelist_view(request)
        if url.endswith('password'):
            return self.user_change_password(request, url.split('/')[0])
        return super(UserAdmin, self).__call__(request, url)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(UserAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults.update({
                'form': self.add_form,
                'fields': admin.util.flatten_fieldsets(self.add_fieldsets),
            })
        defaults.update(kwargs)
        return super(UserAdmin, self).get_form(request, obj, **defaults)

    def get_urls(self):
        from django.conf.urls.defaults import patterns
        return patterns('',
            (r'^(\d+)/password/$', self.admin_site.admin_view(self.user_change_password))
        ) + super(UserAdmin, self).get_urls()

    @csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        # It's an error for a user to have add permission but NOT change
        # permission for users. If we allowed such users to add users, they
        # could create superusers, which would mean they would essentially have
        # the permission to change users. To avoid the problem entirely, we
        # disallow users from adding users if they don't have change
        # permission.
        if not self.has_change_permission(request):
            if self.has_add_permission(request) and settings.DEBUG:
                # Raise Http404 in debug mode so that the user gets a helpful
                # error message.
                raise Http404('Your user does not have the "Change user" permission. In order to add users, Django requires that your user account have both the "Add user" and "Change user" permissions set.')
            raise PermissionDenied
        if extra_context is None:
            extra_context = {}
        defaults = {
            'auto_populated_fields': (),
            'username_help_text': self.model._meta.get_field('username').help_text,
        }
        extra_context.update(defaults)
        return super(UserAdmin, self).add_view(request, form_url, extra_context)

    def user_change_password(self, request, id):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = get_object_or_404(self.model, pk=id)
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                new_user = form.save()
                msg = ugettext('Password changed successfully.')
                messages.success(request, msg)
                return HttpResponseRedirect('..')
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': form.base_fields.keys()})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        return render_to_response(self.change_user_password_template or 'admin/auth/user/change_password.html', {
            'title': _('Change password: %s') % escape(user.username),
            'adminForm': adminForm,
            'form': form,
            'is_popup': '_popup' in request.REQUEST,
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
            'root_path': self.admin_site.root_path,
        }, context_instance=RequestContext(request))

    def response_add(self, request, obj, post_url_continue='../%s/'):
        """
        Determines the HttpResponse for the add_view stage. It mostly defers to
        its superclass implementation but is customized because the User model
        has a slightly different workflow.
        """
        if '_addanother' not in request.POST:
            # The 'Save' button should act like the 'Save and continue
            # editing' button
            request.POST['_continue'] = 1
        return super(UserAdmin, self).response_add(request, obj, post_url_continue)

class UsuarioCardapioAdmin(admin.ModelAdmin):
    list_display = ('cardapio','usuario','data')
    list_filter = ('usuario','cardapio','data')
    raw_id_fields = ['usuario','cardapio']


admin.site.register(Receita, ReceitaAdmin)
admin.site.register(Ingrediente, IngredienteAdmin)
admin.site.register(FuncoesBiologicas)
admin.site.register(Cardapio, CardapioAdmin)
admin.site.register(UsuarioCardapio,UsuarioCardapioAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)
from django.contrib.sites.models import Site
admin.site.unregister(Site)
admin.site.register(User, UserAdmin)
admin.site.register(Nutriente, NutrienteAdmin)