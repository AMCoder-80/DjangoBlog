from django.urls import path
# Importing the django LoginView
from django.contrib.auth.views import LoginView

app_name = 'accounts'

urlpatterns = [
    # Login url
    path('', LoginView.as_view(), name='login'),
]