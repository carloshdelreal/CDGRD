from django.conf.urls import url
from home.views import HomeView, ArticlePhotoDetail

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^articlephoto/(?P<pk>[0-9]+)$', ArticlePhotoDetail.as_view(), name='article_photo'),
]
