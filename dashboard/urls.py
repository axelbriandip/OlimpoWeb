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
    path('members/<int:pk>/edit/', views.member_update_view, name='dashboard_member_update'),
    path('members/<int:pk>/delete/', views.member_delete_view, name='dashboard_member_delete'),
    path('members/add/', views.member_create_view, name='dashboard_member_add'),
    path('news/', views.news_list_view, name='dashboard_news_list'),
    path('news/add/', views.news_create_view, name='dashboard_news_add'),
    path('news/<int:pk>/edit/', views.news_update_view, name='dashboard_news_update'),
    path('news/<int:pk>/delete/', views.news_delete_view, name='dashboard_news_delete'),
    # --- NUEVAS RUTAS PARA GALERÍA ---
    path('gallery/', views.gallery_list_view, name='dashboard_gallery_list'),
    path('gallery/add/', views.gallery_update_view, name='dashboard_gallery_add'),
    path('gallery/<int:pk>/edit/', views.gallery_update_view, name='dashboard_gallery_update'),
    path('gallery/<int:pk>/delete/', views.gallery_delete_view, name='dashboard_gallery_delete'),
]