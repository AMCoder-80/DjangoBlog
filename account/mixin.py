from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from blog.models import Article


# To define custom mixin, you just need to write a python class and overriding builtin cbv methods inside of it
class FieldsSetterMixin:
    # This method is a builtin class base view method, which I override it
    # This method gets a request with its args and return a response, so we can add features between
    # request and response
    def dispatch(self, request, *args, **kargs):
        if request.user.is_superuser:
            self.fields = ["title", "sub_title", "author", "publisher", "reference", "slug", "description", "thumbnail",
                           "status", "category", ]
        elif request.user.is_author:
            self.fields = ["title", "sub_title", "publisher", "reference", "slug", "description", "thumbnail",
                           "category", ]
        else:
            raise HttpResponseForbidden('You are not neither a superuser nor an author')
        # This means that include the codes above in your builtin codes
        return super().dispatch(request, *args, **kargs)

    # This method called when a form is getting submitted to check weather it is valid or not
    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.author = self.request.user
        return super().form_valid(form)


# Another custom mixin to handle the updating access
class UpdateAccess:
    def dispatch(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        if (request.user == article.author and article.status == 'd') or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise HttpResponseNotAllowed("You can not edit this article")


class DeleteAccessMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise HttpResponseNotAllowed("You are not allowed to delete an article")
