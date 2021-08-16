from django.db import models
from django.utils.html import format_html
from django.urls import reverse
# Importing django user model
from account.models import User
from django.utils import timezone
from account.models import IPAddress
from datetime import datetime, timedelta


# Create your models here.

# A class with a desired name which should inherit from models.Manager
# This class's name will be use to defining the manager to django orm
class MyManager(models.Manager):
    # As many function as needed can be write here
    def active_categories(self, instance):
        return self.get(id=instance.id).category.filter(status=True)


class CategoryManager(models.Manager):
    def actives(self):
        return self.filter(status=True)


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.CASCADE,
                               related_name='children')
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    status = models.BooleanField(default=True)
    position = models.IntegerField()
    objects = CategoryManager()

    class Meta:
        ordering = ['position',]

    def __str__(self):
        return self.title


class Article(models.Model):
    CHOICES = (
        ('p', 'published'),
        ('d', 'draft'),
        ('i', 'pending'),
        ('r', 'rejected'),
    )

    title = models.CharField(max_length=50)
    sub_title = models.CharField(max_length=150, null=True, blank=True)
    # Add author col with a one to many relation to the django user with mentioned attributes
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles')
    publisher = models.CharField(max_length=100)
    reference = models.URLField(max_length=150, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    thumbnail = models.ImageField()
    published = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=CHOICES, default='d')
    is_special = models.BooleanField(default=False)


    # This field makes a m2m relation with ip address table which the third table is defined custom with trough attr
    views = models.ManyToManyField(IPAddress, through='ArticleViews', blank=True, related_name='views')

    # The article_set can change by adding this attribute to the relational col
    category = models.ManyToManyField(Category, related_name='articles', blank=True)

    created = models.DateTimeField(auto_now_add=True)

    # The default django manager will over-write by this trick
    objects = MyManager()

    class Meta:
        ordering = ['-created',]

    @property
    def active_categories(self):
        return self.category.filter(status=True)

    def get_absolute_url(self):
        return reverse('accounts:article_list')

    # The last item was the name of this function, now we can define everything we want
    # Notice that the items in list_display passes the object of its own row to our func
    # So we can use that instance of model to make task easier, so we can define this method in
    # admin.py inside the related class or in models.py inside the related model (self must not be added)
    def category_in_string(obj):
        return ', '.join([i.title for i in Article.objects.active_categories(obj)])

    # By defining this method we can return a html code with desired image
    def image_tag(self):
        # format_html avoid showing the code instead of image
        return format_html(f"<img src='{self.thumbnail.url}' width='70' height='50'>")
    # Adding verbose name for methods is possible in this way
    image_tag.short_description = 'Image'

    def __str__(self):
        return self.title


# The third table of views and ip address relation
class ArticleViews(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Article, null=True, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,verbose_name='Reply to'
                               , related_name='replies')
    text = models.TextField(verbose_name='Comment')
    created = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    dislike = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')

    def delta(self):
        differ = self.created - datetime.today()
        if differ.days:
            if differ.days > 30:
                output = f"{differ.days//30} Month ago"
            else:
                output = f"{differ.days} Days ago"

        else:
            if differ.seconds < 60:
                output = 'Just now'
            elif 60 <= differ.seconds < 3600:
                output = f"{differ.seconds//60} Minutes ago"
            else:
                output = f"{differ.seconds//3600} Hours ago"

        return output

    def __str__(self):
        return f"{self.user} => ({self.post})"
