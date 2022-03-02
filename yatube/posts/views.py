from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User
from .utils import get_page_object


def index(request):
    # title = 'Последние обновления на сайте'
    template = 'posts/index.html'
    if 'index_page' in cache:
        post_list = cache.get('index_page')
    else:
        post_list = Post.objects.select_related(
            'author', 'group'
        ).all()
        cache.set('index_page', post_list, 20)
    page_obj = get_page_object(request, post_list)
    context = {
        # 'title': title,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.reverse()
    page_obj = get_page_object(request, post_list)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    title = post.text[:30]
    author = post.author
    author_posts = Post.objects.filter(author=author).select_related(
        'author', 'group'
    )
    count = author_posts.count()
    comments = post.comments.filter(post=post).select_related(
        'author', 'post'
    )
    comment_form = CommentForm()
    context = {
        'post': post,
        'title': title,
        'count': count,
        'comments': comments,
        'form': comment_form
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=post.author)
        context = {'form': form}
        return render(request, 'posts/post_edit.html', context)
    context = {'form': form}
    return render(request, 'posts/post_edit.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post.id)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect('posts:post_detail', post_id=post.id)
    context = {
        'form': form,
        'post': post,
        'is_edit': True,
    }
    return render(request, 'posts/post_edit.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    user = request.user
    authors = user.follower.values_list('author', flat=True)
    post_list = Post.objects.filter(author__in=authors).select_related(
        'author', 'group'
    )
    page_obj = get_page_object(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/follow.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    user = request.user
    post_list = Post.objects.filter(author=author).prefetch_related(
        'author', 'group'
    )
    count = post_list.count()
    page_obj = get_page_object(request, post_list)
    if user.is_authenticated:
        following = Follow.objects.filter(author=author, user=user).exists()
    else:
        following = None
    context = {
        'author': author,
        'count': count,
        'page_obj': page_obj,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    user = request.user
    if author != user:
        Follow.objects.get_or_create(user=user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    user = request.user
    get_object_or_404(Follow, user=user, author=author).delete()
    return redirect('posts:profile', username=username)
