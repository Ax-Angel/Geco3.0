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
from django.urls import include, path
from users.views import *
from corpus.views import *
from apps.concordanciaParalelo.views import *

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register_user_view, name = 'register'),
    path('', index_view, name = 'index'),
    path('dashboard/', user_dashboard_view, name = 'dashboard'),
    path('dashboard/create_project/', create_project_view, name = 'create_project'),
    path('dashboard/add_collaborator/', add_collaborator_view, name = 'add_collaborator'),
    path('list_user_projects/', list_user_projects_view, name = 'list_user_proyects'),
    path('dashboard/upload_document/', document_view.as_view(), name = 'document'),
    path('concordance_paralle/', concordance_paralle_view , name= 'concordance_paralle'),
    path('export/csv/', export_search_csv, name='export_search_csv'),
    path('export/xls/', export_search_xls, name='export_search_xls'),
    path('help/', help_view, name='help_view')
]
