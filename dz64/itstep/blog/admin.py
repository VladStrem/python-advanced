from django.contrib import admin

from .models import Post, Category, Rating

# Register your models here.
admin.site.register(Category)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'publish', 'status']
    list_filter = ['status', 'created', 'publish']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ['publish']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'rating', 'created', 'updated']
    list_filter = ['rating', 'post', 'user']
    search_fields = ['title', 'rating']
    list_display_links = ['id', 'post']
    ordering = ['-created']
