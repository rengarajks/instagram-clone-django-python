from django import forms
from posts.models import Post

class newPostForm(forms.Form):
    picture=forms.ImageField(required=True)
    caption=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'caption'}),required=True)
    tag=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Tag-separated by ,'}),required=True)

    class Meta:
        model=Post
        field=['picture','caption','tag']
