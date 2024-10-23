from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("listings/<int:listing_id>/", views.listing, name="listings"),
    path("new_listing/", views.createlisting, name="new_listing"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:category>/", views.category_listing, name="category_listing"),
    path("listings/<int:id>/watchlist", views.watchlist_add, name = "watchlist_add"),
    path("listings/<int:id>/watchlist/remove", views.watchlist_remove, name = "watchlist_remove"),
]