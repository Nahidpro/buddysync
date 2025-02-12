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


urlpatterns = [
    path('follow/', FollowAPIView.as_view(), name='follow'),
    path('unfollow/', UnfollowAPIView.as_view(), name='unfollow'),
    path('following/', FollowingListAPIView.as_view(), name='following-list'),
    path('followers/', FollowersListAPIView.as_view(), name='followers-list'),
    path('following_count/', FollowingCountAPIView.as_view(), name='following-count'),
    path('followers_count/', FollowersCountAPIView.as_view(), name='followers-count'),
    path('isfollowing/<int:user_id>/', IsFollowingAPIView.as_view(), name='is-following'),
    path('send-request/', SendFriendRequestAPIView.as_view(), name='send-friend-request'),
    path('accept-request/<int:request_id>/', AcceptFriendRequestAPIView.as_view(), name='accept-friend-request'),
    path('reject-request/<int:request_id>/', RejectFriendRequestAPIView.as_view(), name='reject-friend-request'),
    path('requests/', ListFriendRequestsAPIView.as_view(), name='list-friend-requests'),
    path('friends/', ListFriendsAPIView.as_view(), name='list-friends'),
    path('remove-friend/<int:friend_id>/', RemoveFriendAPIView.as_view(), name='remove-friend'),
    path('status/<int:user_id>/', CheckFriendStatusAPIView.as_view(), name='check-friend-status'),
]
