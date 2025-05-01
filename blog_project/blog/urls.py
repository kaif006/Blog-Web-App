from django.urls import path
from . import views

urlpatterns = [
    path("", views.feed, name = "feed"),
    path("profile", views.profile, name = "profile"),
    path("add-post", views.add_post, name = "add-post"),
    path("login", views.login_view, name = "login"),
    path("logout", views.logout_view, name = "logout")
]