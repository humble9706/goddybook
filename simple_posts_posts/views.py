from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from simple_posts_posts.models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from simple_posts_posts.forms import PostCreationForm, CommentCreationForm
from django.utils import timezone 
from django.http import JsonResponse
from simple_posts_posts.utility import Utility
from common.decorators import ajax_required
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action
from django.conf import settings

def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 8)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        posts = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'post_list_ajax.html', {'posts': posts, 'section': 'post_list'})
    return render(request, 'post_list.html', {'posts': posts, 'section': 'post_list'})

@login_required
def post_detail(request, year, month, day, slug, id=None):
    post = get_object_or_404(Post, date__year=year, date__month=month, date__day=day, slug=slug, id=id)
    return render(request, 'post_detail.html', {'post': post, 'section': 'post_detail'})

@login_required
def create_post(request):
    if request.method == 'GET':
        form = PostCreationForm()
    if request.method == 'POST':
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            create_action(request.user, 'created a new post', new_post)
            messages.success(
                request, "Your post '{}'. was uploaded successfully".format(cd['title']))
            return redirect('posts:post_list')
    return render(request, 'create_post.html', {'form': form, 'section': 'make post'})


def create_comment(request, post_id):
    if request.method == 'GET':
        form = CommentCreationForm()
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.writer = request.user
            new_comment.save()
            create_action(request.user, 'added a comment to: ', new_comment.post)
            messages.success(request, "You added a comment to {}'s post: '{}'.".format(post.author, post.title.title()))
            return redirect('posts:post_list')
    return render(request, 'create_comment.html', {'form': form})

@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.likes.add(request.user)
    messages.success(request, "You liked {}'s post: '{}'.".format(post.author, post.title.title()))
    return redirect('posts:post_list')

@login_required
def unlike_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.likes.remove(request.user)
    messages.success(request, "You unliked {}'s post: '{}'.".format(post.author, post.title.title()))
    return redirect('posts:post_list')

@login_required
def comment_list(request, post_id):
    post = Post.objects.get(id = post_id)
    return render(request, 'comment_list.html', {'post': post})

@login_required
def most_liked(request):
    posts = Post.objects.all().order_by('-total_likes', 'date')[0:4]
    return render(request, 'most_liked.html', {'posts': posts, 'section': 'most_liked'})