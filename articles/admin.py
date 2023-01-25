from django.contrib import admin

# Register your models here.
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','id', 'timestamp', 'slug', 'updated']
    search_fields = ['title', 'content']

admin.site.register(Article, ArticleAdmin)