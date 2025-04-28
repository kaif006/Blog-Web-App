from django.shortcuts import render, redirect
from django import forms
from .models import Post
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

# Create your views here.

## view for the feed
def feed(request):
    posts = Post.objects.all()
    return render(request, "blog/feed.html", {
        "home": "home",
        "posts": posts
    })

## form for creatinf post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["image", "caption"]

## view for creating a post
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            test_user = User.objects.get(username='testUser1')  # temperary for testing
            post.author = test_user
            slug = f"post-{get_random_string(5)}"
            post.slug = slug
            post.save()
            return redirect(reverse("feed"))
    else:
        form = PostForm()
    return render(request, "blog/addPost.html")