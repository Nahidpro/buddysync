from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Follow 

User = get_user_model()

class FollowSerializer(serializers.ModelSerializer):
    followed_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    following_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    followed_user_details = serializers.StringRelatedField(source='followed_user')
    following_user_details = serializers.StringRelatedField(source='following_user')

    class Meta:
        model = Follow
        fields = ['followed_user', 'following_user', 'followed_user_details', 'following_user_details']

    def validate(self, data):
       
        if data['followed_user'] == data['following_user']:
            raise serializers.ValidationError("You cannot follow yourself.")
        if Follow.objects.filter(followed_user=data['followed_user'], following_user=data['following_user']).exists():
            raise serializers.ValidationError("You are already following this user.")

        return data