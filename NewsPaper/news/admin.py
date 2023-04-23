from django.contrib import admin
from .models import PostCategory, Post, Comment, Author, Category

# Register your models here.

admin.site.register(PostCategory)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Category)

