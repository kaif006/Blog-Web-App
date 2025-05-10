from django.urls import path
from . import views

urlpatterns = [
    path("", views.feed, name = "feed"),
    path("profile", views.profile, name = "profile"),
    path("add-post", views.add_post, name = "add-post"),
    path("login", views.login_view, name = "login"),
    path("logout", views.logout_view, name = "logout"),
    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('like-status/<int:post_id>/', views.get_like_status, name='like_status')
]