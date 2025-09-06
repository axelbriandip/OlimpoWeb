from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('members/', views.member_list_view, name='dashboard_member_list'),
]