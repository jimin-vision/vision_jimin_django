from django.contrib import admin

from .models import Profile, Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "usage_type", "order", "updated_at")
    search_fields = ("name", "summary")
    list_filter = ("usage_type",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "headline", "email", "updated_at")
    search_fields = ("user__username", "name", "headline", "email")
