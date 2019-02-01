from django.views.generic import TemplateView, DetailView
from .models import Articles, ArticlePhotos
from django.shortcuts import get_object_or_404, get_list_or_404

class HomeView(TemplateView):
    template_name = 'home/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = get_list_or_404(Articles, publicado=True)[:3]
        return context

class ArticlePhotoDetail(DetailView):
    model = ArticlePhotos
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_photo'] = get_object_or_404(Articles, pk=self.kwargs['pk'])
        return context
