from django.contrib import admin
from .models import Article, Category

# Register your models here.



# The last item in list_display doesn't exist in model fields, but we want to declare it
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'writer', 'slug', 'published', 'category_in_string']
    list_filter = ['published', 'created']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ['title',]}
    # This line means the slug filed will be copy automatically from title field
    ordering = ['published', '-writer']
    # Writer filed considered with its first character
    # - Sign means revers order

admin.site.register(Article, ArticleAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'status']
    list_filter = ['status',]
    search_fields = ['title', 'position']
    prepopulated_fields = {'slug': ['title',]}


admin.site.register(Category, CategoryAdmin)
