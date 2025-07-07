from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create_listing, name="create_listing"),
    path("listings/<int:id>/", views.listing_page, name="listing_page"),
    path("listings/<int:id>/add_to_watchlist/", views.add_to_watchlist, name="add_to_watchlist")
]
