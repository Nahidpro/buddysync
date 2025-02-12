from django.urls import path
from .views import PostListCreateView, PostDetailView,FeedView,CommentListCreateView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),

]
