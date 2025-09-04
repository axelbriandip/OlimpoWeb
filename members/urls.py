from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # URLs del Plantel
    path('plantel/', views.player_list, name='player_list'),
    path('plantel/<int:pk>/', views.player_detail, name='player_detail'),
    
    # URLs de Gestión de Socios
    path('quiero-ser-socio/', views.membership_application, name='membership_application'),
    path('login/', auth_views.LoginView.as_view(template_name='members/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # URLs de Páginas Informativas
    path('benefits/', views.benefits, name='benefits'),
    path('costs/', views.costs, name='costs'),
    path('code-of-conduct/', views.code_of_conduct, name='code_of_conduct'),
    path('faq/', views.faq, name='faq'),
    
    # URLs de Reseteo de Contraseña
    # (Añade aquí las 4 URLs de password_reset si las vas a usar)
]