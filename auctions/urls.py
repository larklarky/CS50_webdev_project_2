from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('listing/<int:listing_id>', views.listing, name="listing"),
    path('listing/create', views.create_listing, name='create'),
    path('listing/close/<int:listing_id>', views.closeListing, name='close'),
    path('watchlist/add/<int:listing_id>', views.addToWatchlist, name='watchlist_add'),
    path('watchlist/delete/<int:listing_id>', views.removeFromWatchlist, name='watchlist_delete'),
    path('watchlist', views.watchlist, name='watchlist'),

]
