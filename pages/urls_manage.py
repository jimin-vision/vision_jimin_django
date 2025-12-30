from django.urls import path

from . import manage_views

urlpatterns = [
    path("", manage_views.manage_project_list, name="manage_project_list"),
    path("new/", manage_views.manage_project_create, name="manage_project_create"),
    path("<int:pk>/edit/", manage_views.manage_project_edit, name="manage_project_edit"),
    path("<int:pk>/delete/", manage_views.manage_project_delete, name="manage_project_delete"),
]
