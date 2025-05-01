from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django import forms
from .models import Post
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
    pass