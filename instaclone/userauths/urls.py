from django.urls import path
from .views import EditProfile

urlpatterns=[
    path('editProfile/',EditProfile,name="editprofile")
]