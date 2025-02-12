from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APITestCase, APIClient
from .models import Post  
from connection.models import Follow, Friend
from posts.models import Post, Comment

User = get_user_model()

# class PostListCreateViewTest(APITestCase):
#     def setUp(self):
#         # Create a test user.
#         self.user = User.objects.create_user(username="testuser", password="testpass")
#         # Force authentication for the test client.
#         self.client.force_authenticate(user=self.user)
#         # Define the URL for the PostListCreateView.
#         # Adjust the URL as per your URL configuration.
#         self.url = "/api/posts/"

#     def test_get_posts_paginated(self):
#         """
#         Test that a GET request returns a paginated list of posts.
#         """
#         # Create 10 posts to test pagination (global page size is set to 5).
#         for i in range(10):
#             Post.objects.create(
#                 user=self.user,
#                 content=f"Sample content {i}"
#             )
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#         # The response should include pagination keys: 'count', 'next', 'previous', and 'results'.
#         self.assertIn('count', response.data)
#         self.assertIn('next', response.data)
#         self.assertIn('previous', response.data)
#         self.assertIn('results', response.data)
        
#         # Verify that the first page contains the expected number of posts (5).
#         self.assertEqual(len(response.data['results']), 5)
#         # Verify that the total count is 10.
#         self.assertEqual(response.data['count'], 10)

#     def test_create_post_success(self):
#         """
#         Test that a valid POST request creates a new post.
#         """
#         data = {
#             "content": "Content for the new post"
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # Check that the post data returned is correct.
#         self.assertEqual(response.data["content"], data["content"])
#         # Verify that the created post is associated with the authenticated user.
#         post = Post.objects.get(id=response.data["id"])
#         self.assertEqual(post.user, self.user)

#     def test_create_post_invalid_data(self):
#         """
#         Test that a POST request with invalid data returns a 400 error.
#         """
#         # Assuming 'content' is required, sending an empty content should fail.
#         data = {
#             "content": ""
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         # Optionally, check for a specific error message for the 'content' field.
#         self.assertIn("content", response.data)

#     def test_unauthenticated_access(self):
#         """
#         Test that an unauthenticated request is rejected.
#         """
#         # Remove authentication for this test.
#         self.client.force_authenticate(user=None)
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# class PostDetailViewTest(APITestCase):
#     def setUp(self):
        
#         self.user = User.objects.create_user(username='testuser', password='testpass')
#         self.other_user = User.objects.create_user(username='otheruser', password='testpass')
        
        
#         self.post = Post.objects.create(user=self.user, content='Test post content')
        
        
#         self.detail_url = reverse('post-detail', kwargs={'pk': self.post.id})  

        
#         print(f"Detail URL: {self.detail_url}")

#     def test_get_post_success(self):
#         """Test retrieving a single post successfully."""
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(self.detail_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['content'], self.post.content)

#     def test_get_post_not_found(self):
#         """Test retrieving a non-existing post returns 404."""
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(reverse('post-detail', kwargs={'pk': 9999}))  # Non-existent post ID
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_update_post_success(self):
#         """Test updating a post successfully."""
#         self.client.force_authenticate(user=self.user)
#         response = self.client.put(self.detail_url, {'content': 'Updated content'}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.post.refresh_from_db()
#         self.assertEqual(self.post.content, 'Updated content')

#     def test_update_post_unauthorized(self):
#         """Test that a user cannot update another user's post."""
#         self.client.force_authenticate(user=self.other_user)
#         response = self.client.put(self.detail_url, {'content': 'Hacked content'}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.post.refresh_from_db()
#         self.assertNotEqual(self.post.content, 'Hacked content')

#     def test_delete_post_success(self):
#         """Test deleting a post successfully."""
#         self.client.force_authenticate(user=self.user)
#         response = self.client.delete(self.detail_url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Post.objects.filter(id=self.post.id).exists())

#     def test_delete_post_unauthorized(self):
#         """Test that a user cannot delete another user's post."""
#         self.client.force_authenticate(user=self.other_user)
#         response = self.client.delete(self.detail_url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertTrue(Post.objects.filter(id=self.post.id).exists())


# class FeedViewTestCase(APITestCase):
#     def setUp(self):
#         self.client = APIClient() 

        
#         self.user1 = User.objects.create_user(username="user1", password="pass123")
#         self.user2 = User.objects.create_user(username="user2", password="pass123")
#         self.user3 = User.objects.create_user(username="user3", password="pass123")
#         self.user4 = User.objects.create_user(username="user4", password="pass123")  # Not connected

        
#         Follow.objects.create(following_user=self.user1, followed_user=self.user2)

        
#         Friend.objects.create(from_user=self.user1, to_user=self.user3, status='accepted')

        
#         self.post1 = Post.objects.create(user=self.user1, content="Post by user1")
#         self.post2 = Post.objects.create(user=self.user2, content="Post by user2")
#         self.post3 = Post.objects.create(user=self.user3, content="Post by user3")
#         self.post4 = Post.objects.create(user=self.user4, content="Post by user4")  

#         self.feed_url = reverse('feed')  

#     def authenticate_user(self):
#         """Helper method to authenticate user1"""
#         self.client.force_authenticate(user=self.user1)

#     def test_feed_requires_authentication(self):
#         """Ensure unauthenticated users cannot access the feed"""
#         response = self.client.get(self.feed_url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_feed_shows_correct_posts(self):
#        """Ensure feed shows posts from self, followed users, and friends"""
#        self.authenticate_user()
#        response = self.client.get(self.feed_url)

#        print("Response Status Code:", response.status_code) 
#        print("Response Data:", response.json())  

#        self.assertEqual(response.status_code, status.HTTP_200_OK)

#        response_json = response.json()
#        if isinstance(response_json, dict):  
#         response_json = response_json.get("results", [])

#        post_ids = {post["id"] for post in response_json}

#        expected_posts = {self.post1.id, self.post2.id, self.post3.id}
#        self.assertEqual(post_ids, expected_posts)

#     def test_feed_does_not_show_unrelated_posts(self):
#        """Ensure user does not see posts from unrelated users"""
#        self.authenticate_user() 
#        response = self.client.get(self.feed_url)

      
#        print("Response Status Code:", response.status_code)
#        print("Response Data:", response.json())

#        self.assertEqual(response.status_code, status.HTTP_200_OK)

       
#        response_json = response.json()
#        posts_list = response_json.get("results", [])
#        post_ids = {post["id"] for post in posts_list}
#        self.assertNotIn(self.post4.id, post_ids)



class CommentAPITestCase(APITestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')

        
        self.post = Post.objects.create(user=self.user, content='Test Content')

        
        self.client = APIClient()

    def test_comment_as_follower(self):
        
        Follow.objects.create(followed_user=self.user, following_user=self.other_user)

        
        self.client.force_authenticate(user=self.other_user)

        
        url = f'/api/posts/{self.post.id}/comments/'

        
        response = self.client.post(url, {'content': 'Comment as follower'})

        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().content, 'Comment as follower')

    def test_comment_as_friend(self):
        
        Follow.objects.create(followed_user=self.user, following_user=self.other_user)

        
        self.client.force_authenticate(user=self.other_user)

        
        url = f'/api/posts/{self.post.id}/comments/'

        
        response = self.client.post(url, {'content': 'Comment as friend'})

        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().content, 'Comment as friend')

    def test_comment_as_non_follower_and_non_friend(self):
        
        self.client.force_authenticate(user=self.other_user)

        
        url = f'/api/posts/{self.post.id}/comments/'

        
        response = self.client.post(url, {'content': 'Comment as non-follower and non-friend'})

        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_without_login(self):
        
        url = f'/api/posts/{self.post.id}/comments/'

        response = self.client.post(url, {'content': 'Comment without login'})

        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_comments(self):
        
        Comment.objects.filter(post=self.post).delete()

        
        self.client.force_authenticate(user=self.user)

        
        Comment.objects.create(user=self.user, post=self.post, content='This is a comment')

        
        url = f'/api/posts/{self.post.id}/comments/'

        
        response = self.client.get(url)

        
        print(response.data)

        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
        results = response.data.get("results", [])
        self.assertEqual(len(results), 1)  

        
        self.assertEqual(results[0]['content'], 'This is a comment')