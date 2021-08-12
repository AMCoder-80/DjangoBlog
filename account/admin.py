from django.contrib import admin
from .models import User, IPAddress
from django.contrib.auth.admin import UserAdmin

# Register your models here.

# Overriding the UserAdmin class to customize it as we need to display our own fields
UserAdmin.fieldsets[2][1]['fields'] = (
'is_active', 'is_staff', 'is_superuser', 'is_author', 'special_user', 'groups', 'user_permissions')

# Overriding this attr too, to display the desire value
UserAdmin.list_display += ('is_author', 'is_special_user')

admin.site.register(User, UserAdmin)

admin.site.register(IPAddress)


