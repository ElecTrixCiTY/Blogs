from django.db import models
from django.contrib.auth.models import User

class GalleryModel(models.Model):
    image = models.ImageField(upload_to='gallery')
    uploaded_date = models.DateTimeField(auto_now_add=True)
    owner = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=50, blank=True)
    description =models.CharField(max_length=300, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    