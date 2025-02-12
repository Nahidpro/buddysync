from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Follow , Friend
from django.db import models
from django.db.models import Q

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






class FriendSerializer(serializers.ModelSerializer):
    from_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    to_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Friend
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at', 'updated_at']

    def validate(self, data):
        if data['from_user'] == data['to_user']:
            raise serializers.ValidationError("You cannot send a friend request to yourself.")
        
      
        if Friend.objects.filter(
            (Q(from_user=data['from_user'], to_user=data['to_user']) |
             Q(from_user=data['to_user'], to_user=data['from_user']))
        ).exists():
            raise serializers.ValidationError("A friend request already exists between these users.")
        
        return data