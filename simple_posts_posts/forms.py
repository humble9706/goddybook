from django import forms
from simple_posts_posts.models import Post, Comment


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image', 'title', 'body',)

class CommentCreationForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('body',)