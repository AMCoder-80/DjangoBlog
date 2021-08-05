from django.shortcuts import render
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Article, Category
from django.urls import reverse_lazy
from .models import User
from .forms import ProfileForm
from django.contrib.auth.views import LoginView
from .mixin import FieldsSetterMixin, UpdateAccess, DeleteAccessMixin, SimpleUsersLimitation


# Create your views here.

# Listing Articles for user profile. This view is logged in protected
class ArticleList(SimpleUsersLimitation, ListView):
    template_name = 'AdminLTE/home.html'
    context_object_name = 'articles'

    def get_queryset(self):  # Defining desired queryset
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


# Creating Article view. To access this view, user should be logged in
class ArticleCreate(SimpleUsersLimitation, FieldsSetterMixin, CreateView):
    model = Article
    # Specify the intended fields to be filled out
    template_name = 'AdminLTE/Create_Update.html'


class ArticleUpdate(SimpleUsersLimitation, FieldsSetterMixin, UpdateAccess, UpdateView):
    model = Article
    # Specify the intended fields to be filled out
    template_name = 'AdminLTE/Create_Update.html'


class ArticleDelete(LoginRequiredMixin, DeleteAccessMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('accounts:article_list')
    context_object_name = 'article'
    template_name = 'AdminLTE/Delete.html'


class ArticlePreview(UpdateAccess, DetailView):
    model = Article
    template_name = 'blog/post.html'


class Profile(LoginRequiredMixin, UpdateView):
    template_name = 'AdminLTE/Profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
        })
        return kwargs

# We inherit from default login view to overwrite some changes
class Login(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_author or user.is_superuser:
            return reverse_lazy("accounts:article_list")
        return reverse_lazy("accounts:profile")