from django.urls import path
from .views import (
    FollowAPIView, UnfollowAPIView, FollowingListAPIView, FollowersListAPIView,FollowingCountAPIView, FollowersCountAPIView,IsFollowingAPIView,
    SendFriendRequestAPIView,
    AcceptFriendRequestAPIView,
    RejectFriendRequestAPIView,
    ListFriendRequestsAPIView,
    ListFriendsAPIView,
    RemoveFriendAPIView,
    CheckFriendStatusAPIView
)



