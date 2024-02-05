from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.urls import resolve
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Profile 
from posts.models import Post,Follow,Stream




def UserProfile(request, username):
    
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    posts = Post.objects.filter(user=user).order_by('-posted')

    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favourite.all()
   


     # Profile Stats
    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()

    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    # pagination
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context = {
       
        'posts_paginator':posts_paginator,
        'profile':profile,
        'posts':posts,
        'url_name':url_name,

        'posts_count':posts_count,
        'following_count':following_count,
        'followers_count':followers_count,
        'follow_status':follow_status

        
       
    }
    return render(request, 'profile.html', context)





def follow(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)

    try:
        f, created = Follow.objects.get_or_create(follower=request.user, following=following)

        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=request.user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following)[:25]
            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=request.user, date=post.posted, following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile', args=[username]))

    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))