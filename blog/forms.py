from blog.models import Post, Comment
from ckeditor.widgets import CKEditorWidget
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update({'placeholder': 'Write Comment'})


class PostForm(forms.ModelForm):
    publish_date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('author', 'slug', 'date_posted', 'likes')
