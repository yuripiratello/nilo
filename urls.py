from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin_tools/', include('admin_tools.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),

    url(r'^$','nilo.views.index'),
    (r'^visualizarReceita/(?P<id>\d+)$', 'nilo.views.visualizarReceitas'),
    (r'^alterarSenha/$', 'nilo.views.alterarSenha'),
    #Login/Logout
    url(r'^login/$',  'django.contrib.auth.views.login', {'template_name' : 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url' : '/login/'}, name='logout'),


    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
               {'document_root' : settings.MEDIA_ROOT}),
)
