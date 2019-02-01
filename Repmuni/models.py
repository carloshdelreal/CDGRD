from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.urls import reverse


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100,default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)

class Report(models.Model):
    fenomenos = (
        ('S', 'Sismo'),
        ('R', 'Remoción en Masa'),
        ('I', 'Inundación'),
        ('A', 'Avenida Torrencial'),
        ('I', 'Incendio'),
        ('O', 'Otro')
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    fenomena = models.CharField(max_length=1, choices=fenomenos)
    descrip = models.TextField()
    lat = models.FloatField()
    lng = models.FloatField()
    def __str__(self):
        return "Reporte No: " + str(self.id)
    def get_absolute_url(self):
        return "/repmuni/reporte/{0:%Y}/{0:%m}/{0:%d}/{1}".format(self.created_date,self.id)

class Photos(models.Model):
    image = models.ImageField(upload_to='Report_Photos', blank=False)
    imagedescription = models.TextField(blank=False)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    def __str__(self):
        return "Image: " + self.imagedescription
    def get_absolute_url(self):
        return reverse('repmuni:repmuni_photos', args=[str(self.id)])