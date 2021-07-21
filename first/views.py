# First of all, import the Paginator from the mentioned location
# from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Article, Category


# Create your views here.

class ArticleList(ListView):
    queryset = Article.objects.all().order_by('id')
    template_name = 'first/index.html'
    context_object_name = 'articles'
    paginate_by = 5


# def home(request):
#     numbers_of_articles = Article.objects.all().order_by('id')  # - means reversed direction
#     # Create an instance of paginator by giving the queryset and number of objects in each list
#     pagination = Paginator(numbers_of_articles, 5)
#     # getting the page number over arguments
#     page = request.GET.get('page')
#     # select the desire objects with the page number
#     article = pagination.get_page(page)
#
#     context = {
#         'articles': article,
#     }
#     return render(request, 'first/index.html', context=context)


class ArticleDetail(DetailView):
    template_name = 'first/post.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        return get_object_or_404(Article, slug=self.kwargs.get('slug'))


# def detail(request, slug):
#     article = get_object_or_404(Article, slug=slug)
#
#     context = {
#         'article': article
#     }
#     return render(request, 'first/post.html', context)


class CategoryList(ListView):
    template_name = 'first/category.html'
    paginate_by = 5
    context_object_name = 'articles'

    def get_queryset(self):
        global cat
        slug = self.kwargs.get('slug')
        cat = get_object_or_404(Category.objects.actives(), slug=slug)
        return cat.articles.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = cat
        return context


# def category(request, slug):
#     cat = get_object_or_404(Category, slug=slug, status=True)
#     articles_list = Article.objects.filter(category=cat)
#     pagination = Paginator(articles_list, 3)
#     page = request.GET.get('page')
#     articles = pagination.get_page(page)
#     context = {
#         "category": cat,
#         'articles': articles,
#     }
#     return render(request, 'first/category.html', context)
