from urllib.parse import quote_plus

from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone, translation
from job.filters import JobFilter
from django.utils.translation import gettext as _

from .models import Job, Job_applicant
from django.core.paginator import Paginator
from .forms import ApplyForm, JobForm


# Create your views here.

def job_list(request):
    if request.user.is_authenticated:
        job_list = Job.objects.all().order_by("-published_at")
    else:
        job_list = Job.objects.filter(active=True, publish__lte=timezone.now().date()).order_by("-published_at")

    ## filters
    myfilter = JobFilter(request.GET, queryset=job_list)
    job_list = myfilter.qs

    paginator = Paginator(job_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'jobs': page_obj, 'myfilter': myfilter, 'job_list': job_list, 'title': _('Home')}
    return render(request, 'job/job_list.html', context)


# @permission_required('Job.owner', User.is_superuser)
def job_detail(request, slug):
    job_detail = Job.objects.get(slug=slug)
    share_string = quote_plus(job_detail.description)
    if not job_detail.active or job_detail.publish > timezone.now().date():
        if request.user == job_detail.owner or request.user.is_superuser:
            pass
        else:
            raise Http404

    if request.method == 'POST':
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.job = job_detail
            myform.save()
            messages.success(request, _('Your application has been sent successfully !'))
            return redirect('jobs:job_detail', slug)
    else:
        form = ApplyForm()

    context = {'job': job_detail, 'form1': form, 'title': _('job_detail'), 'share_string': share_string}
    return render(request, 'job/job_detail.html', context)


@login_required
def job_applications(request, id):
    job_applications = Job_applicant.objects.get(id=id)
    context = {'job': job_applications, 'title': _('job_applications')}
    return render(request, 'job/job_applications.html', context)


@login_required
def update_job(request, slug):
    job_detail = Job.objects.get(slug=slug)
    if request.user == job_detail.owner:
        if request.method == 'POST':
            form = JobForm(request.POST, request.FILES, instance=job_detail)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.save()
                slug = new_form.slug
                messages.success(request, _('The job has been updated successfully !'))
                return redirect('jobs:job_detail', slug)
        else:
            form = JobForm(instance=job_detail)

        context = {
            'form': form,
            'job': job_detail,
            'title': _('Update Job')
        }

        return render(request, 'job/update_job.html', context)
    return redirect('jobs:job_detail', slug)


@login_required
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.owner = request.user
            myform.save()
            messages.success(request, _('The job has been add successfully !'))
            return redirect(reverse('jobs:job_list'))
    else:
        form = JobForm()

    return render(request, 'job/add_job.html', {'form': form, 'title': _('Add Job')})


@login_required
def delete_job(request, slug):
    job_detail = Job.objects.get(slug=slug)
    if request.user == job_detail.owner:
        if request.method == 'POST':
            job_detail.delete()
            messages.success(request, _('The job has been deleted successfully !'))
            return redirect('/')
        context = {'job': job_detail, 'title': _('Delete Job')}
        return render(request, 'job/delete_job.html', context)
    return redirect(reverse('jobs:job_detail', slug))


def change_language(request):
    current_language = translation.get_language()
    if current_language == "ar":
        lang_code = "en"
    else:
        lang_code = "ar"

    response = http.HttpResponseRedirect(request.GET.get('return_url'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    translation.activate(lang_code)
    return response
