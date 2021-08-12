from django.db import models

# The user class should inherit from AbstractUser Model from this location
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.


# In this User model, you can append every field you need
class User(AbstractUser):
    is_author = models.BooleanField(default=False)
    special_user = models.DateTimeField(default=timezone.now, verbose_name='Is special user until')

    def is_special_user(self):
        return self.special_user > timezone.now()

    # By this attribute, you can tell django admin to display the method value as a boolean
    is_special_user.boolean = True
    is_special_user.short_description = 'Is special user'


# IPAddress table
class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return self.ip_address

