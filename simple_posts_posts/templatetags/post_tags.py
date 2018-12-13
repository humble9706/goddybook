from django import template
from simple_posts_posts.models import Post

register = template.Library()

@register.inclusion_tag('comment_list.html')
def show_comments(post_id):
	post = Post.objects.get(id = post_id)
	return {'post': post}