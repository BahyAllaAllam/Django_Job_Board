from django.contrib.auth.models import User
from django.db import models
from PIL import Image

# Create your models here.
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext as _
'''
class JobManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(JobManager, self).filter(active=True).filter(publish__lte=timezone.now())

'''


def image_upload(instance, filename):
    extension = filename.split(".")[-1]
    return 'jobs/{}.{}'.format(instance.title, extension)
    # imagename, extension = filename.split(".")
    # return "jobs/%s.%s"%(instance.title, extension)


def file_upload(instance, filename):
    ext = filename.split(".")[-1]
    return 'applicants/{}.{}'.format(instance.name, ext)


class Job(models.Model):
    owner = models.ForeignKey(User, related_name='job_owner', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    job_type = models.CharField(max_length=15, choices=[('Full Time', 'Full Time'), ('Part Time', 'Part Time')])
    description = models.TextField(max_length=1000)
    requirements = models.TextField()
    vacancy = models.IntegerField(default=1)
    salary = models.IntegerField(default=0)
    experience = models.IntegerField(default=1)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    published_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    # objects = JobManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Job, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('jobs:job_detail', kwargs={'slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Job_applicant(models.Model):
    job = models.ForeignKey(Job, related_name='apply_job', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    portfolio_link = models.URLField()
    cv = models.FileField(upload_to=file_upload)
    cover_letter = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('jobs:job_applications', kwargs={'id': self.pk})
