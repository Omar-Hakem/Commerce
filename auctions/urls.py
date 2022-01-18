from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("activeListings", views.activeListings, name="activeListings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("userWatchlist", views.userWatchlist, name="userWatchlist"),
    path("categories", views.categories, name="categories"),
    path(
        "getCategoryListings/<str:category>",
        views.getCategoryListings,
        name="getCategoryListings",
    ),
    path("viewListing/<int:listingId>", views.viewListing, name="viewListing"),
    path("closeAuction/<int:listingId>", views.closeAuction, name="closeAuction"),
    path("addComment/<int:listingId>", views.addComment, name="addComment"),
    path("addToWatchlist/<int:listingId>", views.addToWatchlist, name="addToWatchlist"),
    path(
        "RemoveFromWatchlist/<int:listingId>",
        views.RemoveFromWatchlist,
        name="RemoveFromWatchlist",
    ),
    # path("placeBid/<int:listingId>", views.placeBid, name="placeBid"),
]
