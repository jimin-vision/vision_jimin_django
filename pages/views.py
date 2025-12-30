from django.shortcuts import render

from .data import PROFILE, WORK_USAGE
from .models import Project


def _aggregate_language_usage(projects):
    totals = {}
    for project in projects:
        usage_type = getattr(project, "usage_type", None)
        if usage_type is None and isinstance(project, dict):
            usage_type = project.get("usage_type")
        if usage_type != "language":
            continue

        usage_items = getattr(project, "usage_items", None)
        if usage_items is None and isinstance(project, dict):
            usage_items = project.get("usage_items", [])

        for item in usage_items or []:
            label = item.get("label") if isinstance(item, dict) else None
            percent = item.get("percent") if isinstance(item, dict) else None
            if not label or percent is None:
                continue
            totals[label] = totals.get(label, 0) + float(percent)

    total = sum(totals.values())
    if total <= 0:
        return []

    usage = []
    for label, value in totals.items():
        usage.append({"label": label, "percent": round(value * 100 / total)})

    diff = 100 - sum(item["percent"] for item in usage)
    if usage:
        usage[-1]["percent"] = max(0, usage[-1]["percent"] + diff)
    return usage


def _get_projects(user):
    if not user.is_authenticated:
        return []
    return list(Project.objects.filter(owner=user))


def _build_profile():
    profile = PROFILE.copy()
    email = profile.get("email", "")
    profile["email_link"] = f"mailto:{email}" if email else ""

    github = profile.get("github", "")
    if github and not github.startswith(("http://", "https://")):
        profile["github_link"] = f"https://github.com/{github}"
    else:
        profile["github_link"] = github

    profile["resume_link"] = profile.get("resume", "")
    return profile


def home(request):
    profile = _build_profile()
    projects = _get_projects(request.user)
    language_usage = _aggregate_language_usage(projects)
    context = {
        "profile": profile,
        "projects": projects,
        "language_usage": language_usage,
        "work_usage": WORK_USAGE,
    }
    return render(request, "pages/home.html", context)


def projects(request):
    profile = _build_profile()
    projects = _get_projects(request.user)
    return render(request, "pages/projects.html", {"profile": profile, "projects": projects})


def about(request):
    profile = _build_profile()
    return render(request, "pages/about.html", {"profile": profile})


def contact(request):
    profile = _build_profile()
    return render(request, "pages/contact.html", {"profile": profile})
