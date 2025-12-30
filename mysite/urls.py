from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("pages.urls")),
    path("blog/", include("blog.urls")),
    path("manage/", include("blog.urls_manage")),
    path("admin/", admin.site.urls),
]
