from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my_listings", views.mylistings, name="mylistings"),
    path("my_watchlist", views.watchlist, name="watchlist"),
    path("auctions_won", views.auctions_won, name="auctions_won"),
    path("search_by_category/<str:categoryName>", views.searchByCategory, name="searchByCategory"),
    path("about", views.about, name="about"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<str:listing_id>", views.listing, name="listing"),
    path("commenting/<str:listing_id>", views.listing, name="commenting"),
    path("bidding/<str:listing_id>", views.listing, name="bidding"),
    path("closing/<str:listing_id>", views.listing, name="closing"),
    path("watching", views.watching, name="watching")
]
