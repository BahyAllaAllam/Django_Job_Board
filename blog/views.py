from urllib.parse import quote_plus

from blog import forms
from blog.filters import PostFilter
from blog.forms import CommentForm, PostForm
from blog.models import Post, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.paginator import Paginator
from ckeditor.widgets import CKEditorWidget
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, CreateView
from django.utils.translation import ugettext as _


def post_list(request):
    if request.user.is_authenticated:
        post_list = Post.objects.all().order_by("-published_at")
    else:
        post_list = Post.objects.filter(active=True, publish_date__lte=timezone.now().date()).order_by("-published_at")
    # post_list = Post.objects.all().order_by("-date_posted")
    ## filters
    myfilter = PostFilter(request.GET, queryset=post_list)
    post_list = myfilter.qs
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'posts': page_obj, 'myfilter': myfilter, 'title': _('Blog')}
    return render(request, 'blog/home.html', context)


@login_required
def like_view(request, slug):
    post = get_object_or_404(Post, slug=request.POST.get('post_slug'))
    user = request.user
    if request.method == 'POST':
        post_slug = request.POST.get('post_slug')
        post_obj = Post.objects.get(slug=post_slug)

        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
        else:
            post_obj.likes.add(user)

        post_obj.save()
    return redirect('blog:post-detail', slug)


def post_detail(request, slug):
    post_detail = Post.objects.get(slug=slug)
    if post_detail.active== False or post_detail.publish_date > timezone.now().date():
        if request.user == post_detail.author or request.user.is_superuser:
            pass
        else:
            messages.warning(request, f"You can't access this page please log in first!")
            return redirect('login')

    share_string = quote_plus(post_detail.content)
    comments = post_detail.comments.all()
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the comment to the current post
            new_comment.post_title = post_detail
            # Assign the comment author to the current loged in user
            new_comment.author = request.user
            # Save the comment to the database
            new_comment.save()
            messages.success(request, _('Your comment has been add!'))
            return redirect('blog:post-detail', slug)
    else:
        comment_form = CommentForm()

    context = {'post': post_detail, 'comments': comments, 'new_comment': new_comment, 'form': comment_form,
               'title': _('Blog-{}').format(post_detail), 'share_string': share_string}
    return render(request, 'blog/post_detail.html', context)


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            messages.success(request, _('Your post has been add successfully !'))
            return redirect(reverse('blog:blog-home'))
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {'form': form, 'title': _('Blog-Add Post')})


@login_required
def update_post(request, slug):
    post_detail = Post.objects.get(slug=slug)
    if request.user == post_detail.author:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post_detail)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.save()
                slug = new_form.slug
                messages.success(request, _('Your post has been updated successfully !'))
                return redirect('blog:post-detail', slug)
        else:
            form = PostForm(instance=post_detail)

        context = {
            'form': form,
            'post': post_detail,
            'title': _('Blog-Update {}').format(post_detail)
        }

        return render(request, 'blog/update_post.html', context)
    return redirect('blog:post-detail', slug)


@login_required
def delete_post(request, slug):
    post_detail = Post.objects.get(slug=slug)
    if request.user == post_detail.author:
        if request.method == 'POST':
            post_detail.delete()
            messages.success(request, _('The post has been deleted successfully !'))
            return redirect('/blog/')
        context = {'post': post_detail, 'title': _('Blog-Delete Post {}').format(post_detail)}
        return render(request, 'blog/delete_post.html', context)
    return redirect(reverse('blog:post-detail', slug))


@login_required
def delete_comment(request, slug):
    comment = Comment.objects.get(slug=slug)
    if request.user == comment.author:
        if request.method == 'POST':
            comment.delete()
            return redirect('blog:post-detail', slug)
        context = {'comment': comment, 'title': _('Blog-Delete Comment {}').format(comment)}
        return render(request, 'blog/delete_comment.html', context)
    return redirect(reverse('blog:post-detail', slug))


def about(request):
    return render(request, 'blog/about.html', {'title': _('About')})
