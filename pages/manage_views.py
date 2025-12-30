from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileForm, ProjectForm
from .models import Profile, Project


@login_required
def manage_profile_edit(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={"name": request.user.get_full_name() or request.user.username},
    )
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "소개/연락 정보가 저장되었습니다.")
            return redirect("manage_profile_edit")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "pages/manage/profile_form.html", {"form": form})


@login_required
def manage_project_list(request):
    query = request.GET.get("q", "").strip()
    base_qs = Project.objects.filter(owner=request.user)
    projects = base_qs
    if query:
        projects = projects.filter(Q(name__icontains=query) | Q(summary__icontains=query))
    projects = projects.order_by("order", "-created_at")

    context = {
        "projects": projects,
        "query": query,
        "total_count": base_qs.count(),
    }
    return render(request, "pages/manage/project_list.html", context)


@login_required
def manage_project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            if not project.order:
                project.order = Project.objects.filter(owner=request.user).count() + 1
            project.save()
            messages.success(request, "프로젝트가 저장되었습니다.")
            return redirect("manage_project_list")
    else:
        form = ProjectForm()
    return render(request, "pages/manage/project_form.html", {"form": form, "is_edit": False})


@login_required
def manage_project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "프로젝트가 수정되었습니다.")
            return redirect("manage_project_list")
    else:
        form = ProjectForm(instance=project)
    return render(
        request,
        "pages/manage/project_form.html",
        {"form": form, "project": project, "is_edit": True},
    )


@login_required
def manage_project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == "POST":
        project.delete()
        messages.success(request, "프로젝트가 삭제되었습니다.")
        return redirect("manage_project_list")
    return render(request, "pages/manage/project_confirm_delete.html", {"project": project})
