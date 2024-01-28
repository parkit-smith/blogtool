from typing import Any, Mapping, Optional, Type, Union
from django import forms
from django.forms.utils import ErrorList
from blogpost.models import BlogPost,Ghat
from django.forms import ModelChoiceField

class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self,obj):
        return f'{obj.blog_post_title}'
    

class AddBlogPostForm(forms.ModelForm):
    class Meta:
        model=BlogPost
        fields = '__all__'

class EditBlogPostForm(forms.ModelForm):
    blog_post = MyModelChoiceField(label="Choose blog post to edit",queryset=BlogPost.objects.all())
    class Meta:
        model = BlogPost
        exclude = ('blog_post_title','blog_post_date','blog_post_image','blog_post_text','blog_card_title','blog_card_caption','blog_card_image')

class GitHubAccessTokenForm(forms.ModelForm):
    class Meta:
         model=Ghat
         fields = '__all__'