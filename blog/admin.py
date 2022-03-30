from blog.models import Post, Comment
from django.contrib import admin


# from ckeditor.widgets import CKEditorWidget


class PostAdmin(admin.ModelAdmin):
    list_filter = ['active', 'published_at']
    list_display = ['title', 'published_at', 'active']
    search_fields = ['title', 'content', 'author']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ['post_title', 'author', 'comment']


admin.site.register(Post, PostAdmin)


