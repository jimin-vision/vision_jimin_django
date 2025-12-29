from django.shortcuts import render
from .data import PROFILE, PROJECTS, LANGUAGE_USAGE, WORK_USAGE


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
    context = {
        "profile": profile,
        "projects": PROJECTS,
        "language_usage": LANGUAGE_USAGE,
        "work_usage": WORK_USAGE,
    }
    return render(request, "pages/home.html", context)


def projects(request):
    profile = _build_profile()
    return render(request, "pages/projects.html", {"profile": profile, "projects": PROJECTS})


def about(request):
    profile = _build_profile()
    return render(request, "pages/about.html", {"profile": profile})


def contact(request):
    profile = _build_profile()
    return render(request, "pages/contact.html", {"profile": profile})
