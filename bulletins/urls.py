from django.urls import path, include
from django.contrib.admin.views.decorators import staff_member_required

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('d/<int:pk>/<str:category>/<str:slug>/', views.BulletinDetailView.as_view(), name='bulletin_detail'),
    path('categorias/', views.CategoryIndexView.as_view(), name='category_index'),
    path('categoria/<str:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('equipe/', views.TeamIndexView.as_view(), name='team'),
    path('colaboradores/', views.PartnersIndexView.as_view(), name='partners'),
    path('acoes/', views.ActionIndexView.as_view(), name='actions'),
    path('ajax/add_click', views.add_click, name="add_click"),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('validate-email/', views.validateEmail, name='validateEmail'),
    path('validate-name/', views.validateName, name='validateName'),
    path('cancelar-inscricao/', views.unsubscribe, name='unsubscribe'),
    path('admin/criar-newsletter/', staff_member_required(views.newsletterCreator.as_view()), name="newsletterCreator"),
] 