from django.contrib import admin, messages
from .models import Article, Category
from django.utils.translation import ngettext


# Register your models here.

# Using this decorator to define that this method would be an action
# If no desc added, the method name will be use
@admin.action(description='Activate the categories')
# model_admin => ModelAdmin class that we want to use the action inside of it
# request => The django request object
# queryset => the objects that action should work on
def activate(model_admin, request, queryset):
    # updated => the number of changed objects
    updated = queryset.update(status=True)
    #  ngettxt => help us to define a singular and plural message
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
    # Writer filed considered with its blog character
    # - Sign means revers order


admin.site.register(Article, ArticleAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'parent', 'status']
    list_filter = ['status', ]
    search_fields = ['title', 'position']
    prepopulated_fields = {'slug': ['title', ]}
    # The written action should be used like this
    actions = [inactivate, activate]


admin.site.register(Category, CategoryAdmin)
