from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
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

class GiveProfileCardForm(forms.ModelForm):
	user = forms.ModelChoiceField(queryset = BlogUser.objects.all(), initial=0)
	profile_card = forms.ModelChoiceField(queryset = ProfileCard.objects.all(), initial=0)

	class Meta:
		model = ProfileCardGallery
		fields = ['user', 'profile_card']

class GiveSigilForm(forms.ModelForm):
	user = forms.ModelChoiceField(queryset = BlogUser.objects.all(), initial=0)
	sigil = forms.ModelChoiceField(queryset = Sigil.objects.all(), initial=0)

	class Meta:
		model = SigilGallery
		fields = ['user', 'sigil']

class CreateProfileCardForm(forms.ModelForm):
	name = forms.CharField()
	img = forms.ImageField()
	img_small = forms.ImageField()

	class Meta:
		model = ProfileCard
		fields = ['name', 'img', 'img_small']

class CreateSigilForm(forms.ModelForm):
	name = forms.CharField()
	img = forms.ImageField()
	
	class Meta:
		model = Sigil
		fields = ['name', 'img']
