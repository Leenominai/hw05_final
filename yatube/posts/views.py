from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Group, User, Comment, Follow, posts_limit
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page


def get_paginator(queryset, request):
    paginator = Paginator(queryset, posts_limit)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


# @cache_page(20)
def index(request):
    """Главная страница"""
    template = 'posts/index.html'
    title = 'Последние обновления на сайте'
    page_obj = get_paginator(Post.objects.select_related('group'),
                             request)
    context = {
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    """Страница со списком постов"""
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page_obj = get_paginator(group.posts.all(), request)
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    """Страница профиля пользователя"""
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    page_obj = get_paginator(author.posts.all(), request)
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    """Страница поста"""
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    count = post.author.posts.all().count()
    form = CommentForm(request.POST or None)
    comments = Comment.objects.select_related('post').filter(post=post)
    context = {
        'post': post,
        'count': count,
        'form': form,
        'comments': comments,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    """Страница для публикации постов"""
    template = 'posts/create_post.html'
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user)
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    """Страница для редактирования постов"""
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'form': form,
        'post': post,
        'is_edit': True,
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    """Добавление комментариев к посту"""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """Страница с подписками"""
    template = 'posts/follow.html'
    title = 'Подписки на авторов'
    author_posts = Post.objects.filter(author__following__user=request.user)
    page_obj = get_paginator(author_posts.all(), request)
    context = {
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    """Подписка на автора"""
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    """Отписка от автора"""
    author = get_object_or_404(User, username=username)
    Follow.objects.get(user=request.user, author=author).delete()
    return redirect('posts:profile', username=username)
