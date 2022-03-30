import django_filters
from job.models import Job
from django.utils.translation import gettext as _


class JobFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Job
        fields = '__all__'
        exclude = ['published_at', 'image', 'vacancy', 'owner', 'salary', 'slug', 'publish', 'active', 'updated', 'requirements']
