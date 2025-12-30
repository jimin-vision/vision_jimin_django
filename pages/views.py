from django.shortcuts import render

from .models import Profile, Project


def _aggregate_usage(projects, target_type):
    totals = {}
    for project in projects:
        usage_type = getattr(project, "usage_type", None)
        if usage_type is None and isinstance(project, dict):
            usage_type = project.get("usage_type")
        if usage_type != target_type:
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


def _serialize_profile(profile):
    data = {
        "name": profile.name or profile.user.get_full_name() or profile.user.username,
        "headline": profile.headline,
        "summary": profile.summary,
        "email": profile.email,
        "github": profile.github,
        "resume": profile.resume,
        "focus_language": profile.focus_language,
        "focus_interest": profile.focus_interest,
        "focus_goal": profile.focus_goal,
    }

    email = data.get("email", "")
    data["email_link"] = f"mailto:{email}" if email else ""

    github = data.get("github", "")
    if github and not github.startswith(("http://", "https://")):
        data["github_link"] = f"https://github.com/{github}"
    else:
        data["github_link"] = github

    data["resume_link"] = data.get("resume", "")
    return data


def _get_profile(user):
    if not user.is_authenticated:
        return {}
    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={"name": user.get_full_name() or user.username},
    )
    return _serialize_profile(profile)


def home(request):
    profile = _get_profile(request.user)
    projects = _get_projects(request.user)
    language_usage = _aggregate_usage(projects, Project.USAGE_LANGUAGE)
    work_usage = _aggregate_usage(projects, Project.USAGE_TOOL)
    context = {
        "profile": profile,
        "projects": projects,
        "language_usage": language_usage,
        "work_usage": work_usage,
    }
    return render(request, "pages/home.html", context)


def projects(request):
    profile = _get_profile(request.user)
    projects = _get_projects(request.user)
    return render(request, "pages/projects.html", {"profile": profile, "projects": projects})


def about(request):
    profile = _get_profile(request.user)
    return render(request, "pages/about.html", {"profile": profile})


def contact(request):
    profile = _get_profile(request.user)
    return render(request, "pages/contact.html", {"profile": profile})
