from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post  # Adjust the import as needed

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


class PostDetailViewTest(APITestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.other_user = User.objects.create_user(username='otheruser', password='testpass')
        
        
        self.post = Post.objects.create(user=self.user, content='Test post content')
        
        
        self.detail_url = reverse('post-detail', kwargs={'pk': self.post.id})  

        
        print(f"Detail URL: {self.detail_url}")

    def test_get_post_success(self):
        """Test retrieving a single post successfully."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], self.post.content)

    def test_get_post_not_found(self):
        """Test retrieving a non-existing post returns 404."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('post-detail', kwargs={'pk': 9999}))  # Non-existent post ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post_success(self):
        """Test updating a post successfully."""
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.detail_url, {'content': 'Updated content'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.content, 'Updated content')

    def test_update_post_unauthorized(self):
        """Test that a user cannot update another user's post."""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.put(self.detail_url, {'content': 'Hacked content'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.post.refresh_from_db()
        self.assertNotEqual(self.post.content, 'Hacked content')

    def test_delete_post_success(self):
        """Test deleting a post successfully."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_delete_post_unauthorized(self):
        """Test that a user cannot delete another user's post."""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())