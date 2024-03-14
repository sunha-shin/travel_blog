from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import PostForm, CommentForm  # CommentForm 추가
from .models import Post  # Comment 모델 추가
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def blog_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            messages.success(request, "게시글이 성공적으로 생성되었습니다.")
            return redirect(
                "blog_list"
            )  # 게시글 생성 후에는 blog_list 페이지로 이동합니다.
        else:
            messages.error(
                request, "게시글 생성 중 오류가 발생했습니다. 입력 내용을 확인하세요."
            )
    else:
        form = PostForm()

    return render(request, "blog/blog_create.html", {"form": form})


def blog_list(request):
    is_search = False
    query = request.GET.get("q", "")

    if query:
        posts = (
            Post.objects.filter(
                Q(title__icontains=query) | Q(contents__icontains=query)
            )
            .distinct()
            .order_by("-created_at")
        )
        is_search = True
    else:
        posts = Post.objects.all().order_by("-created_at")

    context = {
        "posts": posts,
        "is_search": is_search,
    }
    return render(request, "blog/blog_list.html", context)


def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()

    comments = post.comments.all()
    new_comment = None

    if request.method == "POST":
        if request.user.is_authenticated:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.author = request.user
                new_comment.save()
                return redirect("blog_detail", pk=post.pk)
            else:
                comment_form = CommentForm()
        else:
            return redirect("login")
    else:
        comment_form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": comment_form,
    }

    return render(request, "blog/blog_detail.html", context)


def blog_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, "You are not allowed to edit this post.")
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect("blog_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, "blog/blog_update.html", {"form": form, "post": post})


@login_required
def blog_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        messages.error(request, "You are not authorized to delete this post.")
        return HttpResponseForbidden("You are not authorized to delete this post.")

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect("blog_list")

    return render(request, "blog/blog_confirm_delete.html", {"post": post})


def blog_search(request):
    query = request.GET.get("q", "")
    search_type = request.GET.get("search_type", "title")  # 검색 유형을 받아옵니다.

    if query:
        if search_type == "title":
            posts = Post.objects.filter(title__icontains=query).distinct()
        elif search_type == "country":
            posts = Post.objects.filter(country__icontains=query).distinct()
        elif search_type == "city":
            posts = Post.objects.filter(city__icontains=query).distinct()
        else:
            # 기본적으로 제목 검색을 수행합니다.
            posts = Post.objects.filter(title__icontains=query).distinct()
    else:
        posts = Post.objects.none()

    context = {
        "posts": posts,
        "query": query,
        "is_search": True,
        "search_type": search_type,  # 검색 유형을 컨텍스트에 추가합니다.
    }
    return render(request, "blog/blog_list.html", context)
