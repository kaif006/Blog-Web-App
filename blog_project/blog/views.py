from django.shortcuts import render

# Create your views here.

def feed(request):
    return render(request, "blog/feed.html", {
        "home": "home"
    })

def add_post(request):
    return render(request, "blog/addPost.html")