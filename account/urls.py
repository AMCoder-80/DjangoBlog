from django.urls import path
# Importing the django LoginView
from django.contrib.auth.views import LoginView
from .views import ArticleList, ArticleCreate

app_name = 'accounts'

urlpatterns = [
    # Login url
    path('login/', LoginView.as_view(), name='login'),
]

urlpatterns += [
    path('', ArticleList.as_view(), name='article_list'),
    path('create/', ArticleCreate.as_view(), name='create_article'),
]