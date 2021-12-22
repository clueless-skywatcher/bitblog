from django.db import router
from django.urls import path

from api.views import *

from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('user/<str:username>/', UserDetailView.as_view({'get': 'retrieve'}, name = 'retrieve-user')),
    path('followers/<str:username>/', UserFollowersView.as_view({'get': 'list'}), name = 'list-user-followers'),
    path('user/<str:username>/gallery/', UserGalleryView.as_view({'get': 'list'}), name = 'list-user-images')
]