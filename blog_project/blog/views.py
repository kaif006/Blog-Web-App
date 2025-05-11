from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django import forms
from .models import Post, Like, Comment
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.db import connection
from django.contrib.auth.decorators import login_required

# Create your views here.

class commentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 2, "placeholder": "Write a comment..."})
        }

## view for the feed
#@login_required(login_url='login')
def feed(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    #posts = Post.objects.all().order_by("-created_date")
    feed_query = """
    SELECT 
        bp.*,
        COUNT(DISTINCT bl.id) * 2 AS like_score,
        COUNT(DISTINCT bc.id) * 3 AS comment_score,
        (
            (1 / (1 + TIMESTAMPDIFF(HOUR, bp.created_date, NOW()))) * 50 +
            COUNT(DISTINCT bl.id) * 2 +
            COUNT(DISTINCT bc.id) * 3
        ) AS feed_score
    FROM 
        blog_post bp
    LEFT JOIN 
        blog_like bl ON bp.id = bl.post_id
    LEFT JOIN 
        blog_comment bc ON bp.id = bc.post_id
    GROUP BY 
        bp.id
    ORDER BY 
        feed_score DESC
    """
    posts = Post.objects.raw(feed_query)
    comment_form = commentForm()

    if request.method == "POST" and "comment_post_id" in request.POST:
        form = commentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = Post.objects.get(id=request.POST["comment_post_id"])
            comment.save()
            return redirect("feed")
    return render(request, "blog/feed.html", {
        "home": "home",
        "posts": posts,
        'comment_form': comment_form
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

