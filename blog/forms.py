from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(PostForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(PostForm, self).save(commit=False)
        inst.author = self._user
        inst.status = 1
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class CreateUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-input'

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
