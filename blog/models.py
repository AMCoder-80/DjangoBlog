from django.db import models
from django.utils.html import format_html
from django.urls import reverse
# Importing django user model
from django.contrib.auth.models import User
from django.utils import timezone


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

    # The article_set can change by adding this attribute to the relational col
    category = models.ManyToManyField(Category, related_name='articles', blank=True)

    created = models.DateTimeField(auto_now_add=True)

    # The default django manager will over-write by this trick
    objects = MyManager()

    @property
    def active_categories(self):
        return self.category.filter(status=True)

    def get_absolute_url(self):
        return reverse('blog:detail_post', args=[self.slug])

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