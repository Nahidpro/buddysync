from django.urls import path
from .views import FollowAPIView, UnfollowAPIView, FollowingListAPIView, FollowersListAPIView,FollowingCountAPIView, FollowersCountAPIView,IsFollowingAPIView
urlpatterns = [
    path('follow/', FollowAPIView.as_view(), name='follow'),
    path('unfollow/', UnfollowAPIView.as_view(), name='unfollow'),
    path('following/', FollowingListAPIView.as_view(), name='following-list'),
    path('followers/', FollowersListAPIView.as_view(), name='followers-list'),
    path('following_count/', FollowingCountAPIView.as_view(), name='following-count'),
    path('followers_count/', FollowersCountAPIView.as_view(), name='followers-count'),
    path('isfollowing/<int:user_id>/', IsFollowingAPIView.as_view(), name='is-following'),
]
