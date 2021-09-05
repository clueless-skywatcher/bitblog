from django.urls import path, include
from .views import *

urlpatterns = [
	path('',  BlogPostListView.as_view(), name = 'blog-home'),
	path('post/<int:pk>/', show_post, name = 'post'),
	path('post/create/', BlogPostCreateView.as_view(), name = 'post-create'),
	path('post/<int:pk>/update/', BlogPostUpdateView.as_view(), name = 'post-update'),
	path('post/<int:pk>/delete/', BlogPostDeleteView.as_view(), name = 'post-delete'),
	path('follow/<int:follower>_<int:followed>', follow_user, name = 'follow-user'),
	path('unfollow/<int:follower>_<int:followed>', unfollow_user, name = 'unfollow-user'),
	path('profile/<str:username>/followers/', show_followers, name = 'show-followers'),
    path('profile/<str:username>/following/', show_following, name = 'show-following'),
    path('search/', SearchUserView.as_view(), name = 'search-user'),
	path('profile-cards/', profile_card_gallery, name = 'profile-cards'),
	path('sigils/', sigil_gallery, name = 'sigils'),
	path('change-profile-card/<str:name>', change_profile_card, name = 'change-profile-card'),
	path('add-profile-card/<str:username>_<int:pk>', add_profile_card, name = 'add-profile-card'),
	path('change-sigil/<str:name>', change_sigil, name = 'change-sigil'),
	path('add-sigil/<str:username>_<int:pk>', add_sigil, name = 'add-sigil'),
	path('give-profilecard/', give_profilecard, name = 'give-profilecard'),
	path('give-sigil/', give_sigil, name = 'give-sigil'),
	path('create-profile-card/', create_profile_card, name = 'create-profile-card'),
	path('create-sigil/', create_sigil, name = 'create-sigil'),
	path('admin/links/', admin_links, name = 'admin-links'),
	path('stats/', stats_dashboard, name = 'stats')
]
