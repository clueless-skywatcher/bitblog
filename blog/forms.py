from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import BlogComment, BlogUser, User
from .blog_enums import *

class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['email']

class CommentForm(forms.ModelForm):
	comment = forms.CharField()

	class Meta:
		model = BlogComment
		fields = ['comment']

class BlogUserUpdateForm(forms.ModelForm):
	desc = forms.CharField(max_length = DESC_SIZE, required = False)
	hometown = forms.CharField(max_length = HOMETOWN_SIZE, required = False)
	birth_date = forms.DateField(required = False)

	class Meta:
		model = BlogUser
		fields = ['desc', 'hometown', 'birth_date']

