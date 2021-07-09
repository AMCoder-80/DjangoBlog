from django.shortcuts import render

from .models import Article


# Create your views here.


def home(request):
    numbers_of_articles = Article.objects.all().order_by('id')[:3]  # - means reversed direction

    context = {
        'articles': numbers_of_articles
    }
    return render(request, 'first/index.html', context=context)
