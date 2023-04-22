from django.shortcuts import render
from django.views.generic import ListView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'flatpages/news.html'
    context_object_name = 'posts'

# Create your views here.
