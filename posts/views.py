from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions,generics
from .models import Post
from .serializers import PostSerializer,CommentSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Post,Comment
from connection.models import Follow, Friend  
from .serializers import PostSerializer
from rest_framework.exceptions import PermissionDenied

# class PostListCreateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         posts = Post.objects.all().order_by('-created_at')
        
#         # Set up pagination
#         paginator = PageNumberPagination()
#         paginator.page_size = 5  # Number of posts per page
#         paginated_posts = paginator.paginate_queryset(posts, request)
        
#         # Serialize paginated data
#         serializer = PostSerializer(paginated_posts, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

    def get(self, request, pk):
        post = self.get_object(pk)
        if not post:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post = self.get_object(pk)
        if not post:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        if post.user != request.user:
            return Response({'error': 'You do not have permission to edit this post'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        if not post:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        if post.user != request.user:
            return Response({'error': 'You do not have permission to delete this post'}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({'message': 'Post deleted'}, status=status.HTTP_204_NO_CONTENT)
    

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id).order_by("-created_at")

    def perform_create(self, serializer):
        post_id = self.kwargs["post_id"]
        post = Post.objects.get(id=post_id)

        
        if not self.is_user_allowed_to_comment(post.user):
            raise PermissionDenied("You are not allowed to comment on this post.")

        serializer.save(user=self.request.user, post=post)

    def is_user_allowed_to_comment(self, post_author):
        
        is_follower = Follow.objects.filter(followed_user=post_author, following_user=self.request.user).exists()
        
        
        is_friend = Friend.objects.filter(
            Q(from_user=post_author, to_user=self.request.user, status='accepted') |
            Q(from_user=self.request.user, to_user=post_author, status='accepted')
        ).exists()

        return is_follower or is_friend


class FeedView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user

        
        following_ids = set(
            Follow.objects.filter(following_user=user).values_list('followed_user_id', flat=True)
        )

        
        friend_tuples = Friend.objects.filter(
            Q(from_user=user) | Q(to_user=user),
            status='accepted'
        ).values_list('from_user_id', 'to_user_id')

        
        friend_ids = {uid for tup in friend_tuples for uid in tup}
        friend_ids.discard(user.id)  

        
        feed_ids = following_ids | friend_ids | {user.id}

        
        return Post.objects.filter(user__id__in=feed_ids) \
                           .order_by('-created_at') \
                           .select_related('user')
    