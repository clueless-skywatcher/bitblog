from collections import OrderedDict

from django.contrib.auth.models import User

from rest_framework import serializers

from api.serializers.ui_serializers import ProfileCardSerializer, SigilSerializer

from blog.models import BlogUser

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    username = serializers.CharField(max_length = 100)
    email = serializers.EmailField()

    def to_representation(self, instance):
        instance = super(UserSerializer, self).to_representation(instance)

        user_dict = {
            'Username': instance['username'],
            'UserID': instance['id'],
            'UserEmail': instance['email']
        }

        return user_dict

    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class BlogUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    desc = serializers.CharField()
    hometown = serializers.CharField()
    birth_date = serializers.DateField()
    user = UserSerializer(read_only = True)
    current_profile_card = ProfileCardSerializer(read_only = True)
    current_sigil = SigilSerializer(read_only = True)
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = BlogUser
        fields = (
            'id', 
            'desc', 
            'hometown', 
            'birth_date', 
            'user', 
            'current_profile_card',
            'current_sigil',
            'followers',
            'following'
        )

    def to_representation(self, instance):
        instance = super(BlogUserSerializer, self).to_representation(instance)

        user_dict = instance['user']
        profile_card_dict = instance['current_profile_card']
        sigil_dict = instance['current_sigil']

        bloguser_dict = {
            'ProfileID': instance['id'],
            'UserID': user_dict['UserID'],
            'Description': instance['desc'],
            'Hometown': instance['hometown'],
            'BirthDate': instance['birth_date'],
            'Username': user_dict['Username'],
            'UserEmail': user_dict['UserEmail'],
            'CurrentProfileCard': profile_card_dict,
            'CurrentSigil': sigil_dict,
            'Followers': instance['followers'],
            'Following': instance['following']
        }

        sorted_dict = OrderedDict()
        sorted_user_keys = sorted(bloguser_dict.keys())
        for key in sorted_user_keys:
            sorted_dict[key] = bloguser_dict[key]

        return sorted_dict

    def get_followers(self, obj):
        return obj.user.followers.count()

    def get_following(self, obj):
        return obj.user.following.count()


    

    




    
