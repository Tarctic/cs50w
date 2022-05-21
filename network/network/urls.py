
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.new_post, name="newpost"),
    path("posts/<str:posts>", views.posts, name="posts"),
    path("user/<str:name>", views.profile, name="profile"),
    path("likes/<int:id>", views.like, name="like"),
    path("edit/<int:id>", views.edit, name="edit")
]
