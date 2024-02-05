from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse


from posts.models import Tag,Stream,Post,Follow,Likes
from userauths.models import Profile
from comment.models import Comment
from comment.forms import NewCommentForm

from .forms import newPostForm
# Create your views here.
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







def newPost(request):
    user=request.user.id
    tag_obj=[]


    if request.method=="POST":
        form=newPostForm(request.POST,request.FILES)
        if form.is_valid():
            picture=form.cleaned_data.get('picture')
            caption=form.cleaned_data.get('caption')
            tag_form=form.cleaned_data.get('tag')
            tag_list=list(tag_form.split(','))

            for tag in tag_list:
                t,created=Tag.objects.get_or_create(title=tag)
                tag_obj.append(t)

            P,created=Post.objects.get_or_create(picture=picture,caption=caption,user_id=user)
            P.tags.set(tag_obj)
            P.save()
            return redirect('index')
        
    else:
        form=newPostForm()

    context={
        'form':form
    }

    return render(request,'newPost.html',context)





def postDetail(request,post_id):
    user=request.user
    post=get_object_or_404(Post,id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-date')

    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('post-detail', args=[post.id]))
    else:
        form = NewCommentForm()
    context={
        'post':post,
        'form': form,
        'comments': comments,
    }

    return render(request,'postdetail.html',context)




def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
        
    post.likes = current_likes
    post.save()
    # return HttpResponseRedirect(reverse('post-details', args=[post_id]))
    return HttpResponseRedirect(reverse('post-detail', args=[post_id]))





def favourite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile=Profile.objects.get(user=user)


    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
        
   
    return HttpResponseRedirect(reverse('post-detail', args=[post_id]))