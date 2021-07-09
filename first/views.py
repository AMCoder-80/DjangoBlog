from django.shortcuts import render, get_object_or_404

from .models import Article


# Create your views here.


def home(request):
    numbers_of_articles = Article.objects.all().order_by('id') # - means reversed direction

    context = {
        'articles': numbers_of_articles
    }
    return render(request, 'first/index.html', context=context)


def detail(request, slug):
    article = get_object_or_404(Article, slug=slug)

    context = {
        'article': article
    }
    return render(request, 'first/post.html', context)
