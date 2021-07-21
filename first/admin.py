from django.contrib import admin, messages
from .models import Article, Category
from django.utils.translation import ngettext


# Register your models here.

@admin.action(description='Activate the categories')
def activate(model_admin, request, queryset):
    updated = queryset.update(status=True)
    model_admin.message_user(request,
                             ngettext(
                                 '%s Category was activated',
                                 '%s Categories were activated',
                                 updated
                             ) % updated, messages.SUCCESS)


@admin.action(description='Inactivate the categories')
def inactivate(model_admin, request, queryset):
    updated = queryset.update(status=False)
    model_admin.message_user(request,
                             ngettext(
                                 '%s Category was inactivated',
                                 '%s Categories were inactivated',
                                 updated
                             ) % updated, messages.SUCCESS
                             )


# The last item in list_display doesn't exist in model fields, but we want to declare it
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag', 'author', 'publisher', 'slug', 'published', 'category_in_string']
    list_filter = ['published', 'created']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ['title', ]}
    # This line means the slug filed will be copy automatically from title field
    ordering = ['published']
    # Writer filed considered with its first character
    # - Sign means revers order


admin.site.register(Article, ArticleAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'parent', 'status']
    list_filter = ['status', ]
    search_fields = ['title', 'position']
    prepopulated_fields = {'slug': ['title', ]}
    actions = [inactivate, activate]


admin.site.register(Category, CategoryAdmin)
