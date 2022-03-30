import django_filters
from blog.models import Post
from django import forms
from django.db import models
from django_filters import DateFromToRangeFilter, DateFilter
from django_filters.widgets import RangeWidget


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    content = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(lookup_expr='icontains')
    publish_date = DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD'}))

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['img', 'active', 'date_posted', 'slug', 'likes', 'published_at', 'updated']

