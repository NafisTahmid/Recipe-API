from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from core.models import Tag
from rest_framework import status

TAGS_URL = reverse('recipe:tag-list')
def create_user():
    return get_user_model().objects.create_user(
        email="user@example.com",
        password="test@123"
    )

class PublicTagsApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
    def test_auth_required(self):
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_all_tags(self):
        
