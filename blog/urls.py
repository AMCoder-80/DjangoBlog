from django.urls import path
from .views import ArticleDetail, CategoryList, ArticleList, AuthorArticles, toggle, com_delete
from django.views.generic import TemplateView
from account.views import ArticlePreview

app_name = 'blog'

urlpatterns = [
    path('', ArticleList.as_view(), name='home_view'),
    path('post/<slug>', ArticleDetail.as_view(), name='detail_post'),
    path('preview/<int:pk>', ArticlePreview.as_view(), name='preview'),
    path('category/<slug>', CategoryList.as_view(), name='categories'),
    path('test/', TemplateView.as_view(template_name='blog/menu.html')),
    path('author/<username>', AuthorArticles.as_view(), name='author'),
    path('toggle-like/', toggle, name='toggling'),
    path('delete-comment/', com_delete, name="com_delete"),
]