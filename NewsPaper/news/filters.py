from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter, CharFilter
from .models import Post, Category, PostCategory
from django.forms import ModelForm
from django.forms import DateInput


class NewsFilter(FilterSet):
    post_category = ModelChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label='Category',
        empty_label='All',
    )
    post_title = CharFilter(
        field_name='title',
        lookup_expr= 'icontains',
        label='Title',
    )
    post_date = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='lt',
        label='Published before',
        widget=DateInput(
            attrs={'type':'datetime-local'},),
        )


#class FormNews(ModelForm):
#    class Meta:
#       model = Post
#       fields = {'title': ['icontains'],
#                 'postCategory':['icontains'],
#                 'dateCreation': ['lt'],

