from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Article, Category


# Create your views here.

# Listing Articles for user profile. This view is logged in protected
class ArticleList(LoginRequiredMixin, ListView):
    template_name = 'AdminLTE/home.html'
    context_object_name = 'articles'

    def get_queryset(self):  # Defining desired queryset
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


# Creating Article view. To access this view, user should be logged in
class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Article
    # Specify the intended fields to be filled out
    fields = ["title", "sub_title", "author", "publisher", "reference", "slug", "description", "thumbnail",
              "category", ]
    template_name = 'AdminLTE/Create_Update.html'
