from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect
from blog.models import Article
from django.conf import settings


# To define custom mixin, you just need to write a python class and overriding builtin cbv methods inside of it
class FieldsSetterMixin:
    # This method is a builtin class base view method, which I override it
    # This method gets a request with its args and return a response, so we can add features between
    # request and response
    def dispatch(self, request, *args, **kargs):
        self.fields = ["title", "sub_title", "publisher", "reference", "slug", "description", "thumbnail",
                       "status", "category", "is_special"]

        if request.user.is_superuser:
            self.fields += ['author']

        # This means that include the codes above in your builtin codes
        return super().dispatch(request, *args, **kargs)

    # This method called when a form is getting submitted to check weather it is valid or not
    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.author = self.request.user
            if form.instance.status != 'i':
                form.instance.status = 'd'
        return super().form_valid(form)


# Another custom mixin to handle the updating access
class UpdateAccess:
    def dispatch(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        if (request.user == article.author and article.status in ['d', 'r']) or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise HttpResponseNotAllowed("You cannot view this page")


class DeleteAccessMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise HttpResponseNotAllowed("You are not allowed to delete an article")


class SimpleUsersLimitation:

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        else:
            if request.user.is_author or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect('accounts:profile')
