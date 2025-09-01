from django.views.generic import ListView, DetailView
from .models import Album

class AlbumListView(ListView):
    model = Album
    template_name = 'gallery/album_list.html'
    context_object_name = 'albums'

class AlbumDetailView(DetailView):
    model = Album
    template_name = 'gallery/album_detail.html'
    context_object_name = 'album'