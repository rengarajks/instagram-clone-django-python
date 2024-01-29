from django.shortcuts import render

from posts.models import    Tag,Stream,Follow,Post

def index(request):
    user=request.user
    posts=Stream.objects.filter(user=user)
    group_ids=[]
    for post in posts:
        group_ids.append(post.post_id)
    post_items=Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    context={
        'post_items':post_items
    }
    return render(request,'index.html',context)