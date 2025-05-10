from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django import forms
from .models import Post, Like
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.db import connection
from django.contrib.auth.decorators import login_required

# Create your views here.

## view for the feed
#@login_required(login_url='login')
def feed(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    posts = Post.objects.all().order_by("-created_date")
    return render(request, "blog/feed.html", {
        "home": "home",
        "posts": posts
    })

def profile(request):
    pass

## form for creatinf post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["image", "caption"]
        widgets = {
            "image": forms.FileInput(attrs={"required": False})
        }

## view for creating a post
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            if not request.FILES.get('image'):
                post.image = None  
            post.author = request.user
            slug = f"post-{get_random_string(5)}"
            post.slug = slug
            post.save()
            return redirect(reverse("feed"))
    else:
        form = PostForm()
    return render(request, "blog/addPost.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("feed"))
        else:
            return render(request, "blog/login.html", {
                "message": "Invalid Username or Password!"
            })

    return render(request, "blog/login.html")
    
def logout_view(request):
    logout(request)
    return render(request, "blog/login.html", {
        "message": "Logged Out"
    })

def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    like, created = Like.objects.get_or_create(user=user, post=post)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'liked': liked,
        'likes_count': Like.objects.filter(post=post).count()
    })

def get_like_status(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    liked = Like.objects.filter(user=user, post=post).exists()
    likes_count = Like.objects.filter(post=post).count()
    return JsonResponse({
        'liked': liked,
        'likes_count': likes_count
    })
