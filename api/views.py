from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers.user_serializers import *
from api.error_enum import HttpErrorEnum

from blog.models import BlogUser, User

class UserDetailView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]

    def retrieve(self, request, username):
        context = {
            'request': self.request
        }
        bloguser = BlogUser.objects.filter(user__username = username).first()
        if not bloguser:
            return Response({
                "Success": False,
                "StatusCode": HttpErrorEnum.HTTP_404_NOT_FOUND.value,
                "ErrorMessage": f"User '{username}' was not found",
                "Error": HttpErrorEnum.HTTP_404_NOT_FOUND.name
            })
        serializer = BlogUserSerializer(bloguser, context = context)
        return Response(serializer.data)

class UserFollowersView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]

    def list(self, request, username):
        context = {
            'request': self.request
        }
        user = User.objects.filter(username = username).first()
        if not user:
            return Response({
                "Success": False,
                "StatusCode": HttpErrorEnum.HTTP_404_NOT_FOUND.value,
                "ErrorMessage": f"User '{username}' was not found",
                "Error": HttpErrorEnum.HTTP_404_NOT_FOUND.name
            })
        
        user_followers = user.followers
        follower_list = []
        for follower in user_followers.all():
            follower_user = follower.follower
            follower_list.append(UserSerializer(follower_user).data)

        follower_count = len(follower_list)

        return Response({
            "FollowerCount": follower_count,
            "FollowersList": follower_list
        })

class UserGalleryView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]

    def list(self, request, username):
        context = {
            'request': self.request
        }
        user = User.objects.filter(username = username).first()
        if not user:
            return Response({
                "Success": False,
                "StatusCode": HttpErrorEnum.HTTP_404_NOT_FOUND.value,
                "ErrorMessage": f"User '{username}' was not found",
                "Error": HttpErrorEnum.HTTP_404_NOT_FOUND.name
            })
        user = user.bloguser

        user_pcards = user.profile_cards
        profile_card_list = []
        for card in user_pcards.all():
            card = card.profile_card
            profile_card_list.append(ProfileCardSerializer(card).data)

        user_sigils = user.sigils
        sigil_list = []
        for card in user_sigils.all():
            card = card.sigil
            sigil_list.append(SigilSerializer(card).data)


        return Response({
            "ProfileCards": profile_card_list,
            "Sigils": sigil_list
        })