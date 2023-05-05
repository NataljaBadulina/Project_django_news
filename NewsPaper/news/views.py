from django.shortcuts import render
from .models import Post
from .filters import NewsFilter
from .forms import PostForm
from django.http import HttpResponseRedirect
from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'flatpages/news.html'
    context_object_name = 'posts'
    paginate_by = 4 # количество записей на странице

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'


def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')

    return render(request, 'flatpages/post_edit.html', {'form': form})
# Create your views here.


# Добавляем новое представление для создания товаров.
class PostCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'flatpages/post_edit.html'


# Добавляем новое представление для создания товаров.
class PostCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель posts
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'flatpages/post_edit.html'


# Добавляем представление для изменения товара.
class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'


# Представление удаляющее товар.
class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_product',)
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('post_list')
