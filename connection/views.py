from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Follow
from .serializers import FollowSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        followed_user_id = request.data.get("followed_user")

        if not followed_user_id:
            return Response({"error": "Followed user ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            followed_user = User.objects.get(id=followed_user_id)
        except User.DoesNotExist:
            return Response({"error": "User to follow does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if followed_user.id == request.user.id:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if Follow.objects.filter(followed_user=followed_user, following_user=request.user).exists():
            return Response({"error": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)

        follow_instance = Follow.objects.create(followed_user=followed_user, following_user=request.user)
        return Response(FollowSerializer(follow_instance).data, status=status.HTTP_201_CREATED)


class UnfollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        followed_user_id = request.data.get("followed_user")

        try:
            followed_user = User.objects.get(id=followed_user_id)
        except User.DoesNotExist:
            return Response({"error": "User to unfollow does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if followed_user.id == request.user.id:
            return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            follow_instance = Follow.objects.get(followed_user=followed_user, following_user=request.user)
        except Follow.DoesNotExist:
            return Response({"error": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)

        follow_instance.delete()
        return Response({"message": "Successfully unfollowed."}, status=status.HTTP_204_NO_CONTENT)


class FollowingListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(following_user=self.request.user).select_related('followed_user')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
  
        response.data['total_following'] = self.get_queryset().count()
        return response


class FollowersListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(followed_user=self.request.user).select_related('following_user')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        response.data['total_followers'] = self.get_queryset().count()
        return response


class FollowingCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following_count = Follow.objects.filter(following_user=request.user).count()
        return Response({"following_count": following_count}, status=status.HTTP_200_OK)


class FollowersCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        followers_count = Follow.objects.filter(followed_user=request.user).count()
        return Response({"followers_count": followers_count}, status=status.HTTP_200_OK)


class IsFollowingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user_to_check = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        is_following = Follow.objects.filter(following_user=request.user, followed_user=user_to_check).exists()
        return Response({"is_following": is_following}, status=status.HTTP_200_OK)