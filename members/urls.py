from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='members/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='members/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('code-of-conduct/', views.code_of_conduct, name='code_of_conduct'),
    path('faq/', views.faq, name='faq'),
    path('benefits/', views.benefits, name='benefits'),
    path('costs/', views.costs, name='costs'),

    # --- RUTAS PARA RESETEO DE CONTRASEÑA ---
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(template_name='members/registration/password_reset_form.html'), 
        name='password_reset'),
    
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='members/registration/password_reset_done.html'), 
        name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='members/registration/password_reset_confirm.html'), 
        name='password_reset_confirm'),

    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='members/registration/password_reset_complete.html'), 
        name='password_reset_complete'),
]