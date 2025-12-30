from django.conf import settings
from django.db import models
from django.utils import timezone


class Project(models.Model):
    USAGE_LANGUAGE = "language"
    USAGE_TOOL = "tool"
    USAGE_OTHER = "other"
    USAGE_CHOICES = [
        (USAGE_LANGUAGE, "Language"),
        (USAGE_TOOL, "Tool"),
        (USAGE_OTHER, "Other"),
    ]

    name = models.CharField(max_length=200)
    summary = models.TextField()
    link = models.URLField(blank=True)
    tech_stack = models.JSONField(default=list, blank=True)
    details = models.JSONField(default=list, blank=True)
    highlights = models.JSONField(default=list, blank=True)
    note = models.TextField(blank=True)
    usage_title = models.CharField(max_length=120, blank=True)
    usage_type = models.CharField(max_length=20, choices=USAGE_CHOICES, blank=True)
    usage_items = models.JSONField(default=list, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
        null=True,
        blank=True,
    )
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    name = models.CharField(max_length=100, blank=True)
    headline = models.CharField(max_length=200, blank=True)
    summary = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    github = models.CharField(max_length=200, blank=True)
    resume = models.URLField(blank=True)
    focus_language = models.CharField(max_length=200, blank=True)
    focus_interest = models.CharField(max_length=200, blank=True)
    focus_goal = models.CharField(max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or self.user.username
