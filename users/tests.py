from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken 

from rest_framework.test import APIClient, APITestCase

from django.urls import reverse

User = get_user_model()

# class RegisterViewTest(APITestCase):
#     def setUp(self):
#         self.register_url = "/api/user/register/"  

#     def test_register_success(self):
#         """Test successful user registration."""
#         data = {
#             "username": "testuser",
#             "email": "test@example.com",
#             "password": "StrongPassword123!",
#             "first_name": "Test",
#             "last_name": "User",
#             "bio": "This is a test user."
#         }
#         response = self.client.post(self.register_url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data["message"], "User registered successfully!")
#         self.assertTrue(User.objects.filter(username="testuser").exists())

#     def test_register_password_validation_failure(self):
#         """Test registration fails due to weak password."""
#         data = {
#             "username": "testuser2",
#             "email": "test2@example.com",
#             "password": "123",  # Weak password
#             "first_name": "Test",
#             "last_name": "User",
#             "bio": "Weak password test."
#         }
#         response = self.client.post(self.register_url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("password", response.data)  # Ensure password validation error is returned

#     def test_register_missing_fields(self):
#         """Test registration fails due to missing required fields."""
#         data = {
#             "username": "testuser3",
#             "password": "StrongPassword123!"
#             # Missing email, first_name, last_name
#         }
#         response = self.client.post(self.register_url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("email", response.data)  # Ensure missing email error is returned
#         self.assertIn("first_name", response.data)  # Ensure missing first name error is returned
#         self.assertIn("last_name", response.data)  # Ensure missing last name error is returned


class ProfileViewTestCase(APITestCase):

    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        
        
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        
        
        self.profile_url = "/api/user/profile/"

    def test_get_profile(self):
        """Test that a user can retrieve their profile data (GET request)."""
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        
        response = self.client.get(self.profile_url)
        
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        self.assertEqual(response.data['username'], self.user.username)

    def test_update_profile_success(self):
        """Test that a user can update their profile data (PUT request)."""
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        
        updated_data = {'username': 'updateduser'}
        
        response = self.client.put(self.profile_url, updated_data)
        
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        self.user.refresh_from_db()  
        self.assertEqual(self.user.username, 'updateduser')

    def test_update_profile_invalid_data(self):
        """Test that invalid data results in a 400 error."""
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        
        
        invalid_data = {'username': ''}
        
        response = self.client.put(self.profile_url, invalid_data)
        
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
        self.assertIn('username', response.data)

    def test_update_profile_no_changes(self):
        """Test that updating with no changes still returns a success response."""
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        
        
        updated_data = {'username': 'testuser'}
        
        response = self.client.put(self.profile_url, updated_data)
        
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser')

    def test_unauthenticated_user_get_profile(self):
        """Test that an unauthenticated user cannot access profile data."""
        response = self.client.get(self.profile_url)
        
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_update_profile(self):
        """Test that an unauthenticated user cannot update profile data."""
        updated_data = {'username': 'newusername'}
        
        response = self.client.put(self.profile_url, updated_data)
        
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_authorization_header(self):
        """Test that invalid authorization headers return a 401 error."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')
        
        response = self.client.get(self.profile_url)
        
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)