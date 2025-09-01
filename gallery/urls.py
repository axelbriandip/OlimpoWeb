from django.urls import path
from .views import AlbumListView, AlbumDetailView

urlpatterns = [
    path('', AlbumListView.as_view(), name='album_list'),
    path('<int:pk>/', AlbumDetailView.as_view(), name='album_detail'),
]