from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Follow,Friend
from .serializers import FollowSerializer,FriendSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import permissions
from uuid import UUID
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound


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
    





############# Friend releted View



class SendFriendRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        to_user_id = request.data.get('to_user_id')
        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

     
        data = {
            'from_user': request.user.id,  
            'to_user': to_user.id
        }

        serializer = FriendSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.exceptions import NotFound

class AcceptFriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        try:
           
            friend_request = Friend.objects.get(id=request_id, status='pending')
        except Friend.DoesNotExist:
            return Response({"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)

        
        if friend_request.to_user != request.user:
            return Response({"error": "You are not authorized to accept this request."}, status=status.HTTP_403_FORBIDDEN)

        
        friend_request.status = 'accepted'
        friend_request.save()

        return Response(FriendSerializer(friend_request).data, status=status.HTTP_200_OK)
    


class RejectFriendRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, request_id):
        try:
            friend_request = Friend.objects.get(id=request_id, to_user=request.user, status='pending')
        except Friend.DoesNotExist:
            return Response({"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)

        friend_request.status = 'rejected'
        friend_request.save()
        return Response({"message": "Friend request rejected."}, status=status.HTTP_200_OK)

class ListFriendRequestsAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendSerializer

    def get_queryset(self):
        return Friend.objects.filter(to_user=self.request.user, status='pending')

class ListFriendsAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendSerializer

    def get_queryset(self):
        return Friend.objects.filter(
            (Q(from_user=self.request.user) | Q(to_user=self.request.user)) &
            Q(status='accepted')
        )



class RemoveFriendAPIView(DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        friend_id = self.kwargs.get('friend_id')

        
        try:
            friend_id = int(friend_id)
        except ValueError:
            raise NotFound("Invalid friend ID. Expected an integer.")

        
        return get_object_or_404(
            Friend,
            (Q(from_user=self.request.user.id, to_user=friend_id) |
             Q(from_user=friend_id, to_user=self.request.user.id)),
            status='accepted'
        )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"detail": "Friend successfully removed."},
            status=status.HTTP_204_NO_CONTENT
        )


class CheckFriendStatusAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        try:
            friend = Friend.objects.get(
                (Q(from_user=request.user, to_user=user_id) |
                 Q(from_user=user_id, to_user=request.user))
            )
            return Response({"status": friend.status}, status=status.HTTP_200_OK)
        except Friend.DoesNotExist:
            return Response({"status": "not_friends"}, status=status.HTTP_200_OK)
