from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('<uuid:post_id>/',views.postDetail,name='post-detail'),
    path('<uuid:post_id>/like',views.like,name='post-like'),
     path('<uuid:post_id>/fav/',views.favourite,name='post-fav'),

    path('newPost/',views.newPost),
    
]
