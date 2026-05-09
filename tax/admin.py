from django.contrib import admin
from .models import Post, FAQ

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_created']
    search_fields = ['title', 'author', 'content']
    ordering = ['-date_created']

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order']
    search_fields = ['question', 'answer']
    ordering = ['order']
