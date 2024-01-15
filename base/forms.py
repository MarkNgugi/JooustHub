from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User, Project, Projectinfo
from django import forms


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'visibility']

class ProjectDetailsForm(forms.ModelForm):
    class Meta:
        model = Projectinfo
        fields = ['heading', 'project_details']
