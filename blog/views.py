from django.shortcuts import render, redirect
from .models import BlogPost, BlogComment, Following, User, ProfileCard, ProfileCardGallery, Sigil, SigilGallery
from .blog_enums import *
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
	current_user = request.user
	following = None
	if current_user.is_authenticated:
		rel_follow = Following.objects.filter(followed = user, follower = current_user).first()
		if rel_follow:
			following = True
		else:
			following = False

	if not user:
		return render(request, 'blog/notfound404.html')
	posts = user.blogpost_set.order_by('-post_date')
	paginator = Paginator(posts, POSTS_PER_PAGE)

	page_no = request.GET.get('page', START_PAGE)

	try:
		page_obj = paginator.page(page_no)
	except PageNotAnInteger:
		page_obj = paginator.page(START_PAGE)
	except EmptyPage:
		page_obj = paginator.page(paginator.num_pages)

	profile_card = user.bloguser.current_profile_card
	sigil = user.bloguser.current_sigil

	return render(request, 'blog/profile.html', context = {
		'profile_user' : user,
		'posts' : posts,
		'following' : following,
		'page_obj' : page_obj,
		'profile_card' : profile_card,
		'sigil' : sigil
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
def follow_user(request, follower, followed):
	followerUser = User.objects.filter(pk = follower).first()
	followedUser = User.objects.filter(pk = followed).first()

	rel_follow = Following.objects.filter(followed = followedUser, follower = followerUser).first()
	if rel_follow is None:
		rel_follow = Following(followed = followedUser, follower = followerUser)
		rel_follow.save()
		messages.success(request, f'You are following {followedUser.username}')
	return redirect('profile', followedUser.username)

@login_required
def unfollow_user(request, follower, followed):
	followerUser = User.objects.filter(pk = follower).first()
	followedUser = User.objects.filter(pk = followed).first()

	rel_follow = Following.objects.filter(followed = followedUser, follower = followerUser).first()
	if rel_follow:
		rel_follow.delete()
		messages.info(request, f'You are no longer following {followedUser.username}')
	return redirect('profile', followedUser.username)

@login_required
def add_profile_card(request, username, pk):
	if not request.user.is_superuser:
		return render(request, 'blog/forbidden403.html')
	profile_card = ProfileCard.objects.filter(pk = pk).first()
	user = User.objects.filter(username = username).first()
	gallery_obj = ProfileCardGallery(user = user.bloguser, profile_card = profile_card)
	gallery_obj.save()
	return redirect('profile', username)

@login_required
def add_sigil(request, username, pk):
	if not request.user.is_superuser:
		return render(request, 'blog/forbidden403.html')
	sigil = Sigil.objects.filter(pk = pk).first()
	user = User.objects.filter(username = username).first()
	gallery_obj = SigilGallery(user = user.bloguser, sigil = sigil)
	gallery_obj.save()
	return redirect('profile', username)

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

@login_required
def profile_card_gallery(request):
	current_user = request.user
	profile_cards = sorted([p.profile_card for p in current_user.bloguser.profile_cards.all()], key = lambda x : x.name)
	return render(request, 'blog/profcard_gallery.html', context = {
		'profile_cards' : profile_cards
	})

@login_required
def change_profile_card(request, name):
	user = request.user
	profile_card = ProfileCard.objects.filter(name = name).first()
	user.bloguser.current_profile_card = profile_card
	user.save()
	return redirect('profile', user.username)

@login_required
def change_sigil(request, name):
	user = request.user
	sigil = Sigil.objects.filter(name = name).first()
	user.bloguser.current_sigil = sigil
	user.save()
	return redirect('profile', user.username)

@login_required
def sigil_gallery(request):
	current_user = request.user
	sigils = sorted([s.sigil for s in current_user.bloguser.sigils.all()], key = lambda x : x.name)
	return render(request, 'blog/sigil_gallery.html', context = {
		'sigils' : sigils,
		'large' : True
	})

class BlogPostListView(ListView):
	model = BlogPost
	template_name = 'index.html'
	context_object_name = 'posts'
	ordering = ['-post_date']
	paginate_by = 20

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

def show_followers(request, username):
	p_user = User.objects.filter(username = username).first()
	followers = p_user.followers.all()
	return render(request, 'blog/followlist.html', context = {
		'followlist' : followers,
		'header' : 'Followers',
		'p_user' : p_user,
		'following' : False
	})

def show_following(request, username):
	p_user = User.objects.filter(username = username).first()
	following = p_user.following.all()
	return render(request, 'blog/followlist.html', context = {
		'followlist' : following,
		'header' : 'Following',
		'p_user' : p_user,
		'following' : True
	})

class SearchUserView(ListView):
	model = User
	template_name = 'blog/search_user.html'
	context_object_name = 'users'

	def get_queryset(self):
		query = self.request.GET.get('searchkey')
		return User.objects.filter(username__contains = query)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['searchkey'] = self.request.GET.get('searchkey')
		return context
