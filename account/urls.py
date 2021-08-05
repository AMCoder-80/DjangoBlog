from django.urls import path, reverse_lazy
# Importing the django LoginView
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from .views import *

app_name = 'accounts'

urlpatterns = [
    # Login url
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', PasswordChangeView.as_view(success_url=reverse_lazy('accounts:password_change_done'),
                                                        template_name='blog/password_change_form.html'),
         name='password_change'),
    path('change-password/done', PasswordChangeDoneView.as_view(template_name='blog/password_change_done.html'),
         name='password_change_done'),
]

urlpatterns += [
    path('', ArticleList.as_view(), name='article_list'),
    path('create/', ArticleCreate.as_view(), name='create_article'),
    path('update/<int:pk>', ArticleUpdate.as_view(), name='update_article'),
    path('delete/<int:pk>', ArticleDelete.as_view(), name='delete_article'),
    path('profile/', Profile.as_view(), name='profile'),
]
