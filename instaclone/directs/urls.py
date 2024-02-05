from django.urls import path
from . import views
from .views import Directs

urlpatterns=[
    path('inbox/',views.inbox,name="directs"),
    path('directs/<username>',Directs,name="directs"),
    path('send/',views.SendDirect,name="send-message")
]