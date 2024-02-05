from django.contrib import admin
from . import models
from userauths.models import Profile
from comment.models import Comment
# Register your models here.


admin.site.register(models.Tag)
admin.site.register(models.Post)
admin.site.register(models.Follow)
admin.site.register(models.Stream)

admin.site.register(Comment)
admin.site.register(Profile)