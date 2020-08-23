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
    path('profile/<str:username>/following/', show_following, name = 'show-following')
]
