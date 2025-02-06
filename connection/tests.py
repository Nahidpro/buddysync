from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Friend ,Follow

User = get_user_model()

# class FollowAPITestCase(APITestCase):
#     def setUp(self):
#         # Create two users
#         self.user1 = User.objects.create_user(username="user1", password="testpass")
#         self.user2 = User.objects.create_user(username="user2", password="testpass")
        
#         # Force authentication for user1
#         self.client.force_authenticate(user=self.user1)
        
#         # Use the correct URL (with trailing slash)
#         self.follow_url = "/api/connection/follow/"

#     def test_follow_success(self):
#         """Test if a user can successfully follow another user."""
#         response = self.client.post(self.follow_url, {"followed_user": self.user2.id})
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(Follow.objects.filter(followed_user=self.user2, following_user=self.user1).exists())

#     def test_cannot_follow_self(self):
#         """Test that a user cannot follow themselves."""
#         response = self.client.post(self.follow_url, {"followed_user": self.user1.id})
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data["error"], "You cannot follow yourself.")

#     def test_follow_non_existent_user(self):
#         """Test that following a non-existent user returns 404."""
#         response = self.client.post(self.follow_url, {"followed_user": 9999})  # ID that doesn't exist
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_cannot_follow_twice(self):
#         """Test that a user cannot follow another user twice."""
#         Follow.objects.create(followed_user=self.user2, following_user=self.user1)
#         response = self.client.post(self.follow_url, {"followed_user": self.user2.id})
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data["error"], "You are already following this user.")

#     def test_unauthenticated_cannot_follow(self):
#         """Test that an unauthenticated user cannot follow others."""
#         # Remove authentication for this test
#         self.client.force_authenticate(user=None)
#         response = self.client.post(self.follow_url, {"followed_user": self.user2.id})
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
class UnfollowAPITestCase(APITestCase):
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username="user1", password="testpass")
        self.user2 = User.objects.create_user(username="user2", password="testpass")
        
        
        self.client.force_authenticate(user=self.user1)
        
        
        self.unfollow_url = "/api/connection/unfollow/"

    def test_unfollow_success(self):
        """Test that a user can successfully unfollow another user."""
     
        Follow.objects.create(followed_user=self.user2, following_user=self.user1)
        
        response = self.client.post(self.unfollow_url, {"followed_user": self.user2.id})
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        self.assertFalse(Follow.objects.filter(followed_user=self.user2, following_user=self.user1).exists())

    def test_unfollow_not_following(self):
        """Test that unfollowing a user that is not being followed returns an error."""
        response = self.client.post(self.unfollow_url, {"followed_user": self.user2.id})
       
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "You are not following this user.")

    def test_unfollow_self(self):
        """Test that a user cannot unfollow themselves."""
        response = self.client.post(self.unfollow_url, {"followed_user": self.user1.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "You cannot unfollow yourself.")

    def test_unfollow_non_existent_user(self):
        """Test that unfollowing a non-existent user returns 404."""
        
        response = self.client.post(self.unfollow_url, {"followed_user": 9999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "User to unfollow does not exist.")

    def test_unauthenticated_cannot_unfollow(self):
        """Test that an unauthenticated user cannot unfollow."""
        
        self.client.force_authenticate(user=None)
        response = self.client.post(self.unfollow_url, {"followed_user": self.user2.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


###### test Friend API
# class AcceptFriendRequestTestCase(APITestCase):

#     def setUp(self):
#         # Create users for testing
#         self.user1 = User.objects.create_user(username="user1", password="testpassword")
#         self.user2 = User.objects.create_user(username="user2", password="testpassword")

#         # Generate JWT token for the first user
#         refresh = RefreshToken.for_user(self.user1)
#         self.access_token = str(refresh.access_token)

#         # Create a pending friend request from user1 to user2
#         self.friend_request = Friend.objects.create(
#             from_user=self.user1,
#             to_user=self.user2,
#             status='pending'
#         )

#     def test_accept_friend_request(self):
#     # Log in as user1 (who sent the request, NOT the recipient)
#       refresh_user1 = RefreshToken.for_user(self.user1)
#       access_token_user1 = str(refresh_user1.access_token)

#       url = f"/api/connection/accept-request/{self.friend_request.id}/"

#     # Send POST request as user1 (who should NOT be able to accept)
#       response = self.client.post(
#         url,
#         HTTP_AUTHORIZATION=f'Bearer {access_token_user1}'
#     )

#     # Check for 403 Forbidden (user1 should not be allowed to accept their own request)
#       self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#       self.assertEqual(response.data['error'], 'You are not authorized to accept this request.')

#     def test_accept_friend_request_not_found(self):
#         # Test the case where the friend request is not found
#         url = "/api/connection/accept-request/999/"  # Invalid request ID

#         # Send POST request with the correct JWT token
#         response = self.client.post(
#             url,
#             HTTP_AUTHORIZATION=f'Bearer {self.access_token}'  # Pass JWT token for user1
#         )

#         # Check that the status is 404 Not Found
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data['error'], 'Friend request not found.')

#     def test_accept_friend_request_wrong_user(self):
#     # Log in as user1 (who should NOT be able to accept the request)
#       refresh_user1 = RefreshToken.for_user(self.user1)
#       access_token_user1 = str(refresh_user1.access_token)

#       url = f"/api/connection/accept-request/{self.friend_request.id}/"

#     # Send POST request as user1 (who is the sender, not receiver)
#       response = self.client.post(
#         url,
#         HTTP_AUTHORIZATION=f'Bearer {access_token_user1}'
#     )

#     # Check that it now correctly returns 403 Forbidden
#       self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#       self.assertEqual(response.data['error'], 'You are not authorized to accept this request.')


# class RejectFriendRequestTestCase(APITestCase):
#     def setUp(self):
#         # Create users
#         self.user1 = User.objects.create_user(username="user1", password="testpassword")
#         self.user2 = User.objects.create_user(username="user2", password="testpassword")
        
#         # Generate JWT token for user2 (recipient of friend request)
#         refresh = RefreshToken.for_user(self.user2)
#         self.access_token = str(refresh.access_token)
        
#         # Create a pending friend request from user1 to user2
#         self.friend_request = Friend.objects.create(
#             from_user=self.user1,
#             to_user=self.user2,
#             status='pending'
#         )

#     def test_reject_friend_request(self):
#         url = f"/api/connection/reject-request/{self.friend_request.id}/"
        
#         response = self.client.post(
#             url,
#             HTTP_AUTHORIZATION=f'Bearer {self.access_token}'  # Pass JWT token
#         )
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.friend_request.refresh_from_db()
#         self.assertEqual(self.friend_request.status, 'rejected')
#         self.assertEqual(response.data["message"], "Friend request rejected.")

#     def test_reject_non_existent_friend_request(self):
#         url = "/api/connection/reject-request/9999/"  # Non-existent request
        
#         response = self.client.post(
#             url,
#             HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
#         )
        
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data["error"], "Friend request not found.")

#     def test_reject_friend_request_wrong_user(self):
#         # Log in as a different user who is not the recipient
#         refresh = RefreshToken.for_user(self.user1)
#         access_token = str(refresh.access_token)
        
#         url = f"/api/connection/reject-request/{self.friend_request.id}/"
        
#         response = self.client.post(
#             url,
#             HTTP_AUTHORIZATION=f'Bearer {access_token}'  # User1 should not be able to reject
#         )
        
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.friend_request.refresh_from_db()
#         self.assertEqual(self.friend_request.status, 'pending')


# class RemoveFriendTestCase(APITestCase):

#     def setUp(self):
#         # Create users
#         self.user1 = User.objects.create_user(username="user1", password="testpassword")
#         self.user2 = User.objects.create_user(username="user2", password="testpassword")
#         self.user3 = User.objects.create_user(username="user3", password="testpassword")  # Not a friend

#         # Create a friend connection
#         self.friendship = Friend.objects.create(from_user=self.user1, to_user=self.user2, status="accepted")

#         # Generate JWT tokens
#         refresh1 = RefreshToken.for_user(self.user1)
#         self.user1_token = str(refresh1.access_token)

#         refresh2 = RefreshToken.for_user(self.user2)
#         self.user2_token = str(refresh2.access_token)

#         refresh3 = RefreshToken.for_user(self.user3)
#         self.user3_token = str(refresh3.access_token)

#         self.url = "/api/connection/remove-friend/{friend_id}/"

#     def test_remove_friend_success(self):
#         """Test if a user can successfully remove a friend"""
#         response = self.client.delete(
#             self.url.format(friend_id=self.user2.id),
#             HTTP_AUTHORIZATION=f'Bearer {self.user1_token}'
#         )
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Friend.objects.filter(id=self.friendship.id).exists())

#     def test_remove_non_existent_friend(self):
#         """Test if removing a non-existent friend returns a 404"""
#         response = self.client.delete(
#             self.url.format(friend_id=9999),
#             HTTP_AUTHORIZATION=f'Bearer {self.user1_token}'
#         )
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_remove_friend_not_connected(self):
#         """Test if a user can't remove someone who is not their friend"""
#         response = self.client.delete(
#             self.url.format(friend_id=self.user3.id),
#             HTTP_AUTHORIZATION=f'Bearer {self.user1_token}'
#         )
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_unauthorized_access(self):
#         """Test if unauthenticated users can't remove a friend"""
#         response = self.client.delete(self.url.format(friend_id=self.user2.id))
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
# class SendFriendRequestTestCase(APITestCase):

#     def setUp(self):
#         # Create users
#         self.user1 = User.objects.create_user(username="user1", password="testpassword")
#         self.user2 = User.objects.create_user(username="user2", password="testpassword")

#         # Generate JWT tokens
#         refresh1 = RefreshToken.for_user(self.user1)
#         self.user1_token = str(refresh1.access_token)

#         self.url = "/api/connection/send-request/"

#     def test_send_friend_request_success(self):
#         """Test if a user can successfully send a friend request"""
#         response = self.client.post(
#             self.url,
#             {"to_user_id": self.user2.id},
#             HTTP_AUTHORIZATION=f'Bearer {self.user1_token}'
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(Friend.objects.filter(from_user=self.user1, to_user=self.user2, status="pending").exists())

#     def test_send_friend_request_to_non_existent_user(self):
#         """Test sending a friend request to a non-existent user"""
#         response = self.client.post(
#             self.url,
#             {"to_user_id": 9999},
#             HTTP_AUTHORIZATION=f'Bearer {self.user1_token}'
#         )
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_send_friend_request_to_self(self):
#         """Test sending a friend request to oneself"""
#         response = self.client.post(
#             self.url,
#             {"to_user_id": self.user1.id},
#             HTTP_AUTHORIZATION=f'Bearer {self.user1_token}'
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_send_duplicate_friend_request(self):
#         """Test sending a duplicate friend request"""
#         Friend.objects.create(from_user=self.user1, to_user=self.user2, status="pending")

#         response = self.client.post(
#             self.url,
#             {"to_user_id": self.user2.id},
#             HTTP_AUTHORIZATION=f'Bearer {self.user1_token}'
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_unauthenticated_user_cannot_send_request(self):
#         """Test if an unauthenticated user is blocked from sending friend requests"""
#         response = self.client.post(self.url, {"to_user_id": self.user2.id})
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)




