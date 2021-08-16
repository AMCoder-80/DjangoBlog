# First of all, import the Paginator from the mentioned location
# from django.core.paginator import Paginator
from account.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Article, Category, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import SpecialUserOnlyMixin
from django.http import HttpResponse
from .forms import CommentForm
from django.core.mail import send_mail
from Learning.settings import EMAIL_HOST_USER as sender


# Create your views here.

# Article list inherit from ListView
class ArticleList(LoginRequiredMixin, ListView):
    queryset = Article.objects.filter(status='p')  # Defined queryset
    template_name = 'blog/index.html'  # Template name
    context_object_name = 'articles'  # context name used for template engine
    paginate_by = 5  # Pagination py 5 article in each page


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
#     return render(request, 'blog/index.html', context=context)

# Separate articles view inherit from Detail View
class ArticleDetail(SpecialUserOnlyMixin, DetailView):
    template_name = 'blog/post.html'  # Template name
    context_object_name = 'article'  # Context name used for template engine

    def get_object(self, queryset=None):  # Defining required queryset
        global article
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article.objects.filter(status='p'), slug=slug)
        # Access the user ip address via ip_address attr
        ip = self.request.user.ip_address

        # Checks weather ip address is the article viewers or not
        if ip not in article.views.all():
            article.views.add(ip)

        return article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def post(self, *args, **kwargs):
        article = Article.objects.get(slug=kwargs.get('slug'))
        form = CommentForm(self.request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = self.request.user
            comment.post = article
            comment.save()

            author_email = article.author.email
            try:
                parent_email = comment.parent.user.email
            except:
                parent_email = None

            if author_email != parent_email and author_email != comment.user.email:
                message_author = f"""
                Hi {article.author.username},
                user {comment.user.username}, has left a comment recently to you {article.title} article.
                Check it out answer if necessary.
                Have a nice time
                """
                send_mail('New Comment', message_author, sender, [author_email, ])

            if parent_email:
                message_parent = f"""
                Hi {comment.parent.user.username},
                user {comment.user.username}, has replied to your comment in {article.title} article.
                Check it out and answer it if necessary.
                Have a nice time
                """
                send_mail('New Reply', message_parent, sender, [parent_email, ])

        return redirect(self.request.path + "#refer")


# def detail(request, slug):
#     article = get_object_or_404(Article, slug=slug)
#
#     context = {
#         'article': article
#     }
#     return render(request, 'blog/post.html', context)

# Category list
class CategoryList(ListView):
    template_name = 'blog/category.html'
    paginate_by = 5
    context_object_name = 'articles'

    def get_queryset(self):  # Defining required queryset
        global cat
        slug = self.kwargs.get('slug')
        cat = get_object_or_404(Category.objects.actives(), slug=slug)
        return cat.articles.all()

    def get_context_data(self, *, object_list=None, **kwargs):  # Overriding context data
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
#     return render(request, 'blog/category.html', context)

class AuthorArticles(ListView):
    paginate_by = 5
    template_name = 'blog/author.html'
    context_object_name = 'articles'

    def get_queryset(self):
        global user
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return Article.objects.filter(author=user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = user
        return context


def toggle(request):
    state = request.GET['state']
    operation = request.GET['operation']
    user = request.GET['user']
    id = request.GET['pk']
    comment = Comment.objects.get(id=id)

    try:
        if state == '-like':
            if operation == 'sub':
                comment.like.remove(int(user))
            elif operation == 'add':
                comment.like.add(int(user))
            elif operation == 'double':
                comment.dislike.remove(int(user))
                comment.like.add(int(user))

        elif state == '-dislike':
            if operation == 'sub':
                comment.dislike.remove(int(user))
            elif operation == 'add':
                comment.dislike.add(int(user))
            elif operation == 'double':
                comment.like.remove(int(user))
                comment.dislike.add(int(user))

        return HttpResponse('True')
    except:
        return HttpResponse('Error occurred')


def com_delete(request):
    pk = request.GET.get('pk')
    comment = Comment.objects.get(pk=pk)
    comment.delete()
    return HttpResponse('OK')
