from django.contrib import admin
from .models import PostCategory, Post, Comment, Author, Category


class CategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = (CategoryInline, )


admin.site.register(PostCategory)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Category)

