from django.shortcuts import render, redirect
from .models import BlogPost, BlogComment
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, CommentForm, BlogUserUpdateForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import (
	ListView, 
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home_page(request):
	posts = BlogPost.objects.order_by('-post_date')
	return render(request, 'index.html', context = {
		'title' : "BitBlog - Home",
		'posts' : posts,
		'current_user' : request.user
	})

def register_page(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"Registered user: {username}. You can now log in.")
			return redirect('login')
	else:
		form = UserRegistrationForm()
	return render(request, 'blog/register.html', context = {
		'form' : form
	})

def profile(request, username):
	user = User.objects.filter(username = username).first()
	posts = user.blogpost_set.order_by('-post_date')
	return render(request, 'blog/profile.html', context = {
		'profile_user' : user,
		'posts' : posts
	})

def show_post(request, pk):
	post = BlogPost.objects.filter(id = pk).first()
	comments = post.blogcomment_set.order_by('-comment_date')
	
	if request.method == 'POST':
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			post = BlogPost.objects.filter(id = pk).first()
			user = request.user
			comment = comment_form.cleaned_data.get('comment')
			comm_obj = BlogComment(
				comment = comment,
				author = user,
				parent_post = post 
			)
			comm_obj.save()
		return redirect('post', pk = pk)
	else:
		comment_form = CommentForm()

	return render(request, 'blog/post.html', context = {
		'post' : post,
		'comments' : comments,
		'comment_form' : comment_form,
		'current_user' : request.user
	})

@login_required
def update_user(request):
	if request.method == 'POST':
		update_form = UserUpdateForm(request.POST, instance = request.user)
		profile_form = BlogUserUpdateForm(request.POST, instance = request.user.bloguser)
		if update_form.is_valid() and profile_form.is_valid():
			update_form.save()
			profile_form.save()
			messages.success(request, 'Your account has been updated')
			return redirect('profile', username = request.user.username)
	else:
		update_form = UserUpdateForm(instance = request.user)
		profile_form = BlogUserUpdateForm(instance = request.user.bloguser)

	context = {
		'update_form' : update_form,
		'uname' : request.user.username,
		'profile_form' : profile_form
	}
	return render(request, 'blog/update_profile.html', context = context)

# @login_required
# def make_comment(request, pk):
# 	post = BlogPost.objects.filter(id = pk).first()
# 	if request.method == 'POST':
# 		comment_form = CommentForm(request.POST)
# 		if comment_form.is_valid():
# 			post = BlogPost.objects.filter(id = pk).first()
# 			user = request.user
# 			comment = form.cleaned_data.get('comment')
# 			comm_obj = BlogComment(
# 				comment = comment,
# 				author = user,
# 				parent_post = post 
# 			)
# 			comm_obj.save()
# 		return redirect('post', pk = pk)
# 	else:
# 		comment_form = CommentForm()

# 	return render(request, 'blog/post.html', context = {
# 		'post' : post,
# 		'comment_form' : comment_form
# 	})
			
class BlogPostListView(ListView):
	model = BlogPost
	template_name = 'index.html'
	context_object_name = 'posts'
	ordering = ['-post_date']

class BlogPostCreateView(LoginRequiredMixin, CreateView):
	model = BlogPost
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = BlogPost
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = BlogPost
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

