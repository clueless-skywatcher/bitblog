from collections import OrderedDict

from rest_framework import serializers

from blog.models import ProfileCard, Sigil

class ProfileCardSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()
    img = serializers.URLField()

    class Meta:
        model = ProfileCard
        fields = ('id', 'name', 'img')

    def to_representation(self, instance):
        instance = super(ProfileCardSerializer, self).to_representation(instance)

        prof_card_dict = {
            "ProfileCardID": instance['id'],
            "ProfileCardName": instance['name'],
            "ProfileCardImgURL": instance['img']
        }

        sorted_dict = OrderedDict()
        sorted_keys = sorted(prof_card_dict.keys())
        for key in sorted_keys:
            sorted_dict[key] = prof_card_dict[key]


        return sorted_dict

class SigilSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()
    img = serializers.URLField()

    class Meta:
        model = Sigil
        fields = ('id', 'name', 'img')

    def to_representation(self, instance):
        instance = super(SigilSerializer, self).to_representation(instance)

        sigil_dict = {
            "SigilID": instance['id'],
            "SigilName": instance['name'],
            "SigilImgURL": instance['img']
        }

        sorted_dict = OrderedDict()
        sorted_keys = sorted(sigil_dict.keys())
        for key in sorted_keys:
            sorted_dict[key] = sigil_dict[key]

        return sorted_dict