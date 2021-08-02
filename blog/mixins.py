from django.shortcuts import get_object_or_404
from .models import Article


class SpecialUserOnlyMixin:

    def dispatch(self, request, *args, **kwargs):
        article = get_object_or_404(Article.objects.filter(status='p'), slug=kwargs.get('slug'))
        if article.is_special:
            if request.user == article.author or request.user.is_superuser or request.user.is_special_user():
                self.template_name = 'blog/post.html'
            else:
                self.template_name = 'AdminLTE/special_user.html'

        return super().dispatch(request, *args, **kwargs)