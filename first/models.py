from django.db import models
from django.utils import timezone


# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=50)
    sub_title = models.CharField(max_length=150, null=True, blank=True)
    writer = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    thumbnail = models.ImageField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
