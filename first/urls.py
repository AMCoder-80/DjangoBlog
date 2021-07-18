from django.urls import path
from .views import home, detail, category
from django.views.generic import TemplateView

app_name = 'blog'

urlpatterns = [
    path('', home, name='home_view'),
    path('post/<slug>', detail, name='detail_post'),
    path('category/<slug>', category, name='categories'),
    path('test/', TemplateView.as_view(template_name='first/menu.html')),
]