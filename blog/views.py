from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import PostForm
from .models import Post


def post_list(request):
    posts = Post.objects.filter(status=Post.STATUS_PUBLISHED).order_by("-created_at")
    return render(request, "blog/post_list.html", {"posts": posts})


@login_required
def manage_post_list(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "all")

    posts = Post.objects.all().order_by("-created_at")
    if status == Post.STATUS_PUBLISHED:
        posts = posts.filter(status=Post.STATUS_PUBLISHED)
    elif status == Post.STATUS_DRAFT:
        posts = posts.filter(status=Post.STATUS_DRAFT)

    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    paginator = Paginator(posts, 8)
    page_obj = paginator.get_page(request.GET.get("page"))

    params = request.GET.copy()
    params.pop("page", None)
    query_string = params.urlencode()

    context = {
        "posts": page_obj.object_list,
        "page_obj": page_obj,
        "query": query,
        "status": status,
        "total_count": Post.objects.count(),
        "published_count": Post.objects.filter(status=Post.STATUS_PUBLISHED).count(),
        "draft_count": Post.objects.filter(status=Post.STATUS_DRAFT).count(),
        "query_string": query_string,
    }
    return render(request, "blog/manage/post_list.html", context)


@login_required
def manage_post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "글이 저장되었습니다.")
            return redirect("manage_post_list")
    else:
        form = PostForm()
    return render(request, "blog/manage/post_form.html", {"form": form, "is_edit": False})


@login_required
def manage_post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "글이 수정되었습니다.")
            return redirect("manage_post_list")
    else:
        form = PostForm(instance=post)
    return render(request, "blog/manage/post_form.html", {"form": form, "post": post, "is_edit": True})


@login_required
def manage_post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        messages.success(request, "글이 삭제되었습니다.")
        return redirect("manage_post_list")
    return render(request, "blog/manage/post_confirm_delete.html", {"post": post})


@login_required
@require_POST
def manage_post_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.status == Post.STATUS_PUBLISHED:
        post.status = Post.STATUS_DRAFT
        message = "글을 비공개로 전환했습니다."
    else:
        post.status = Post.STATUS_PUBLISHED
        message = "글을 공개로 전환했습니다."
    post.save()
    messages.info(request, message)

    next_url = request.POST.get("next")
    return redirect(next_url or "manage_post_list")
