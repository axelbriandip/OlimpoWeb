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
    
    # --- RUTAS PARA RESETEO DE CONTRASEÑA (ASEGÚRATE DE QUE ESTÉN AQUÍ) ---
    path(
        'password-reset/', 
        auth_views.PasswordResetView.as_view(template_name='members/registration/password_reset_form.html'), 
        name='password_reset'
    ),
    path(
        'password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='members/registration/password_reset_done.html'), 
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='members/registration/password_reset_confirm.html'), 
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='members/registration/password_reset_complete.html'), 
        name='password_reset_complete'
    ),
]
