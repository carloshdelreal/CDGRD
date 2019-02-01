from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Articles(models.Model):

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    pub_date = models.DateField()
    headline = models.CharField(max_length=200)
    content = models.TextField()
    thumb = models.ImageField(upload_to='article_thumbs', blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publicado = models.BooleanField()

    def __str__(self):
        return self.headline

class ArticlePhotos(models.Model):
    image = models.ImageField(upload_to='article_images', blank=False)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    def __str__(self):
        return "Image: " + self.id
    def get_absolute_url(self):
        return reverse('home:article_photo', args=[str(self.id)])