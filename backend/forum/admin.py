from django.contrib import admin
from .models import Tag, Post, Image, Reply

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'tags']
    search_fields = ['title', 'content']
    filter_horizontal = ['images', 'tags', 'products']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['file', '__str__']
    search_fields = ['file']

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['content', 'author', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content']