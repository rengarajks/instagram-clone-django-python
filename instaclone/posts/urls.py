from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('<uuid:post_id>/',views.postDetail,name='post-detail'),

    path('newPost/',views.newPost),
    
]
