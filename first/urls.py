from django.urls import path
from .views import home, detail, category

app_name = 'blog'

urlpatterns = [
    path('', home, name='home_view'),
    path('post/<slug>', detail, name='detail_post'),
    path('category/<slug>', category, name='categories'),
]