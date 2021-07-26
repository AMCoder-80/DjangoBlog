from django.urls import path
from .views import ArticleDetail, CategoryList, ArticleList, AuthorArticles
from django.views.generic import TemplateView

app_name = 'blog'

urlpatterns = [
    path('', ArticleList.as_view(), name='home_view'),
    path('post/<slug>', ArticleDetail.as_view(), name='detail_post'),
    path('category/<slug>', CategoryList.as_view(), name='categories'),
    path('test/', TemplateView.as_view(template_name='blog/menu.html')),
    path('author/<username>', AuthorArticles.as_view(), name='author'),
]