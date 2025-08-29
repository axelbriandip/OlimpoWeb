from django.views.generic import ListView, DetailView
from .models import Article, NewsCategory

class ArticleListView(ListView):
    model = Article
    template_name = 'news/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        # El queryset base siempre son los artículos publicados.
        queryset = Article.objects.filter(status='PB')
        
        # Verificamos si se pasó una categoría en la URL para filtrar.
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        return queryset

    def get_context_data(self, **kwargs):
        # Obtenemos el contexto base.
        context = super().get_context_data(**kwargs)
        
        # Añadimos la lista de todas las categorías para poder crear los botones de filtro.
        context['categories'] = NewsCategory.objects.all()
        
        # Guardamos la categoría seleccionada para resaltar el botón activo.
        context['selected_category_slug'] = self.request.GET.get('category')
        
        return context

class ArticleDetailView(DetailView):
    """
    Muestra el contenido completo de un único artículo y una lista de artículos recomendados.
    """
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        # Nos aseguramos de que solo se pueda acceder a artículos publicados.
        return Article.objects.filter(status='PB')

    def get_context_data(self, **kwargs):
        # Obtenemos el contexto base
        context = super().get_context_data(**kwargs)
        
        # Obtenemos el artículo actual que se está mostrando
        current_article = self.get_object()
        
        # Buscamos otros artículos en la misma categoría, excluyendo el actual.
        # Los ordenamos por fecha para mostrar los más recientes y tomamos hasta 3.
        recommended_articles = Article.objects.filter(
            status='PB',
            category=current_article.category
        ).exclude(
            id=current_article.id
        ).order_by('-created_on')[:3]
        
        # Añadimos la lista de artículos recomendados al contexto
        context['recommended_articles'] = recommended_articles
        
        return context
