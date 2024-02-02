from django.shortcuts import render,redirect

from posts.models import Tag,Stream,Post,Follow

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