from django.contrib import admin, messages
from .models import Article, Category, Comment
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


@admin.action(description='Draft Articles')
def make_draft(model_admin, request, queryset):
    updated = queryset.update(status='d')
    model_admin.message_user(request,
                             ngettext(
                                 '%s Article was drafted',
                                 '%s Articles were drafted',
                                 updated
                             ) % updated, messages.SUCCESS
                             )


@admin.action(description='Publish Articles')
def publish(model_admin, request, queryset):
    updated = queryset.update(status='p')
    model_admin.message_user(request,
                             ngettext(
                                 '%s Article was published',
                                 '%s Articles were published',
                                 updated
                             ) % updated, messages.SUCCESS
                             )


# The last item in list_display doesn't exist in model fields, but we want to declare it
class ArticleAdmin(admin.ModelAdmin):
    #      Image_tag refers to thumbnail renderer method in models
    list_display = ['title', 'image_tag', 'author', 'publisher', 'slug', 'is_special', 'status', 'category_in_string']
    list_filter = ['published', 'created', 'status']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ['title', ]}
    # This line means the slug filed will be copy automatically from title field
    actions = [make_draft, publish]
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
admin.site.register(Comment)
