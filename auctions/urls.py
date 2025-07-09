from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create_listing, name="create_listing"),
    path("listings/<int:id>/", views.listing_page, name="listing_page"),
    path("listings/<int:id>/add_to_watchlist/", views.add_to_watchlist, name="add_to_watchlist"),
    path("listings/<int:id>/remove_from_watchlist/", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("listings/<int:id>/close", views.close_auction_listing, name="close_auction_listing"),
    path("listings/<int:listing_id>/comment/", views.comment_on_listing, name="comment"),
    path("watchlist/", views.watchlist_page, name="watchlist")
]
