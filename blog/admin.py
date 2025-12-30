from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "status", "updated_at")
    search_fields = ("title", "content")
    list_filter = ("status",)
