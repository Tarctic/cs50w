from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>/", views.newpage, name="page"),
    path("search/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("<str:name>/edit/", views.edit, name="edit"),
    path("random/", views.rand, name="rand")
]
