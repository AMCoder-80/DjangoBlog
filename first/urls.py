from django.urls import path
from .views import home

urlpatterns = [
    path('articles/', home, name='home_view')
]