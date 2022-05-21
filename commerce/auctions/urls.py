from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.listings, name="listing"),
    path("item/<int:listing_id>/", views.item, name="item"), #Remember to add <str:name> for specific pages of the same kind (otherwise : "NoReverseMatch")
    path("watchlist", views.wishlist, name="wishlist"),
    path("category/<str:cat>/", views.category, name="category")
]
