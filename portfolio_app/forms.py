from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import Project, Student, Portfolio

#create class for project form
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields ='__all__'

#create class for project form
class PortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        fields ='__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude =['user', 'portfolio']