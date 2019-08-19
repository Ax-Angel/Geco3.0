"""GECO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.conf.urls import url

from django.contrib.auth.decorators import login_required

from users.views import *
from corpus.views import *
from apps.concordanciaParalelo.views import *

urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/register/', register_user_view, name = 'register'),
    url(r'^$', index_view, name = 'index'),
    
    url(r'^dashboard$', user_dashboard_view, name = 'dashboard'),
    url(r'^dashboard/create_project/', Project_Create.as_view(), name = 'create_project'),
    url(r'^dashboard/delete_project/(?P<pk>\d+)/$', login_required(Project_Delete.as_view()), name='delete_project'),
    #path('dashboard/create_project/', create_project_view, name = 'create_project'),
    
    url(r'^dashboard/add_collaborator/', add_collaborator_view, name = 'add_collaborator'),
    url(r'^list_user_projects/', list_user_projects_view, name = 'list_user_proyects'),
    url(r'^dashboard/upload_document/', document_view.as_view(), name = 'document'),
    
    url(r'^concordance_paralle$', concordance_paralle_view , name= 'concordance_paralle'),
    url(r'^export/csv$', export_search_csv, name='export_search_csv'),
    url(r'^export/xls$', export_search_xls, name='export_search_xls'),
    
    url(r'^help$', help_view, name='help_view'),
    url(r'^applications$', apps_view, name='applications'),
    
    url(r'^reset/password_reset',
        auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', 
                                             email_template_name='registration/password_reset_email.html'), 
        name='password_reset'),
    url(r'^reset/password_reset_done',
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/done',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'),
]
