from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('members/', views.member_list_view, name='dashboard_member_list'),
    path('billing/', views.billing_dashboard_view, name='dashboard_billing'),
    path('billing/approve/<int:invoice_id>/', views.approve_payment, name='approve_payment'),
    path('billing/reject/<int:invoice_id>/', views.reject_payment, name='reject_payment'),
    path('billing/items/new/', views.billable_item_create, name='billable_item_create'),
    path('billing/items/<int:pk>/edit/', views.billable_item_update, name='billable_item_update'),
    path('billing/items/<int:pk>/delete/', views.billable_item_delete, name='billable_item_delete'),
]