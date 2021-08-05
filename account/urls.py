from django.urls import path, reverse_lazy
# Importing the django LoginView
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from .views import *

app_name = 'accounts'


urlpatterns = [
    path('', ArticleList.as_view(), name='article_list'),
    path('create/', ArticleCreate.as_view(), name='create_article'),
    path('update/<int:pk>', ArticleUpdate.as_view(), name='update_article'),
    path('delete/<int:pk>', ArticleDelete.as_view(), name='delete_article'),
    path('profile/', Profile.as_view(), name='profile'),
]
