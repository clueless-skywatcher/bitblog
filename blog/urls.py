from django.urls import path, include
from .views import *

urlpatterns = [
	path('',  BlogPostListView.as_view(), name = 'blog-home'),
	path('post/<int:pk>/', show_post, name = 'post'),
	path('post/create/', BlogPostCreateView.as_view(), name = 'post-create'),
	path('post/<int:pk>/update/', BlogPostUpdateView.as_view(), name = 'post-update'),
	path('post/<int:pk>/delete/', BlogPostDeleteView.as_view(), name = 'post-delete')
]