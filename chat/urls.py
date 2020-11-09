from django.urls import path
from chat import views

urlpatterns = [
    path('', views.chat_index, name = "chat-index"),
    path('<str:room_name>/', views.chat_room, name = "chat-room")
]