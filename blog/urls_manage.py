from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import ManageLoginForm

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="blog/manage/login.html", authentication_form=ManageLoginForm
        ),
        name="manage_login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="manage_login"), name="manage_logout"),
    path("", views.manage_post_list, name="manage_post_list"),
    path("new/", views.manage_post_create, name="manage_post_create"),
    path("<int:pk>/edit/", views.manage_post_edit, name="manage_post_edit"),
    path("<int:pk>/delete/", views.manage_post_delete, name="manage_post_delete"),
    path("<int:pk>/toggle/", views.manage_post_toggle, name="manage_post_toggle"),
]
