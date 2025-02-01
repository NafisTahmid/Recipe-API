from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
# JWT_TOKEN_URL = reverse('user:user_login')
# POST_CREATE_URL = reverse('user:create_post')
ME_URL = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email address exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password is less than 5 characters."""
        payload = {
            'email': 'test@example.com',
            'password': '5',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'name': "Test Name",
            'email': "test@example.com",
            'password': "test@123"
        }
        # Create the user with valid details
        create_user(**user_details)  # Create the user
        payload = {
            "email": user_details["email"],
            "password": user_details["password"]
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)  # Check if 'token' is included
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(email="test@example.com", password="goodpass")
        payload = {
            "email": "test@example.com",
            "password": "badpass"
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test returns error if password is blank."""
        payload = {
            "email": "test@example.com",
            "password": ""
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        "Returns false for unauthorized users"
        response = self.client.post(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""
    def setUp(self):
        self.user = create_user(
            email= "test@example.com",
            password = "test@123",
            name = "Test Name",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_retrieve_profile_success(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Testing post method is not allowed for ME URL"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        payload = {
            'name': 'Updated name',
            'password': 'updatedPassword'
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

# """Testing users using jwt tokens"""
# class JWTAuthenticationTests(APITestCase):
#     def setUp(self):
#         """Create a test user for authentication"""
#         self.user_data = {
#             "name": "Test name",
#             "email": "test@example.com",
#             "password": "test@123"
#         }
#         self.user = get_user_model().objects.create_user(**self.user_data)
    

#     def get_jwt_token(self):
#       """Helper function to obtain JWT token for test user"""
#       response = self.client.post(JWT_TOKEN_URL, {
#           'email':self.user_data['email'],
#           'password':self.user_data['password']
#       })
#       return response.data['access']
    
#     def test_jwt_token_obtain(self):
#         response = self.client.post(JWT_TOKEN_URL, {
#             'email': self.user_data['email'],
#             'password':self.user_data['password']
#         })
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('refresh', response.data)
#         self.assertIn('access', response.data)

#     def test_jwt_authentication_required(self):

         
#         name = 'test user'
#         username = 'testuser'
#         email = 'test@beet.com'
#         address = {
#             'street':'Demo street',
#             'suite': 'Demo suite',
#             'city': 'Unknown city',
#             'zipcode': 'xxxx-1234',
#             'geo': {
#                 'lat': 'test lat',
#                 'lng': 'test lng'
#             }
#         }
#         phone = 'demo-phone'
#         website = 'demo-website'
#         company = {
#             'name': 'Demo company',
#             'catchPhrase': 'test phrase',
#             'bs': 'test bs'
#         }

#         demo_user = {
        
#             'name':name,
#             'username':username,
#             'email':email,
#             'address':address,
#             'phone':phone,
#             'website':website,
#             'company':company
#          }
#         response = self.client.post(POST_CREATE_URL, json=demo_user)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_jwt_authentication_successful(self):
#         access_token = self.get_jwt_token()
#         config = {'Authorization': f"Bearer {access_token}"}
#         name = 'test user'
#         username = 'testuser'
#         email = 'test@beet.com'
#         address = {
#             'street':'Demo street',
#             'suite': 'Demo suite',
#             'city': 'Unknown city',
#             'zipcode': 'xxxx-1234',
#             'geo': {
#                 'lat': 'test lat',
#                 'lng': 'test lng'
#             }
#         }
#         phone = 'demo-phone'
#         website = 'demo-website'
#         company = {
#             'name': 'Demo company',
#             'catchPhrase': 'test phrase',
#             'bs': 'test bs'
#         }

#         demo_user = {
        
#             'name':name,
#             'username':username,
#             'email':email,
#             'address':address,
#             'phone':phone,
#             'website':website,
#             'company':company
#          }
#         response = self.client.post(POST_CREATE_URL, json=demo_user, **config)


