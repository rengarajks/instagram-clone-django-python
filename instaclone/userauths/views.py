from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.urls import resolve
from django.contrib.auth.models import User

from .models import Profile 
from posts.models import Post



def UserProfile(request, username):
    
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    posts = Post.objects.filter(user=user).order_by('-posted')

    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favourite.all()
   
    # pagination
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context = {
       
        'posts_paginator':posts_paginator,
        'profile':profile,
        'posts':posts,
        'url_name':url_name
        
       
    }
    return render(request, 'profile.html', context)