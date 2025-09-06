from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('members/', views.member_list_view, name='dashboard_member_list'),
    path('billing/', views.billing_dashboard_view, name='dashboard_billing'),
    path('billing/approve/<int:payment_id>/', views.approve_payment, name='approve_payment'),
]
