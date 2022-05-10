from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from ckeditor.fields import RichTextField
from django.utils.text import slugify


def image_upload(instance, filename):
    ext = filename.split(".")[-1]
    return 'blog/{}.{}'.format(instance.title, ext)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    img = models.ImageField(upload_to=image_upload)
    slug = models.SlugField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='post_likes')
    publish_date = models.DateField(auto_now=False, auto_now_add=False)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    published_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    @property
    def num_likes(self):
        return self.likes.all().count()


class Comment(models.Model):
    post_title = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.post_title)
        super(Comment, self).save(*args, **kwargs)

    class Meta:
        ordering = ('date_posted',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.author, self.post_title)
