from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from .helpers import *


class GalleryModel(models.Model):
    image = models.ImageField(upload_to='gallery')
    uploaded_date = models.DateTimeField(auto_now_add=True)
    owner = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    link = models.URLField(null=True, blank=True)


class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField()
    slug = models.SlugField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='blog_photos')
    uploaded_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(Blog, self).save(*args, **kwargs)


class ContactModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()