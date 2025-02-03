from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from core.models import Tag
from rest_framework import status
from recipe.serializers import TagSerializer
from rest_framework.settings import api_settings

TAGS_URL = reverse('recipe:tag-list')
def create_user(email="user@example.com", password="test@123"):
    return get_user_model().objects.create_user(
        email=email,
        password=password
    )

def detail_url(tag_id):
    return reverse('recipe:tag-detail', args=[tag_id])

class PublicTagsApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
    def test_auth_required(self):
        """Test auth is required for retrieving tags"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)
        # api_settings.DEFAULT_PAGINATION_CLASS = None

    def test_retrieve_all_tags(self):
        """Test retrieve all tags"""
        Tag.objects.create(user=self.user, name="Dairy")
        Tag.objects.create(user=self.user, name="Veggies")
        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tag_limited_to_user(self):
        user_two = create_user(email="user2@example.com")
        Tag.objects.create(user=user_two, name="fruity")
        tag = Tag.objects.create(user=self.user, name="Protien")
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

    
    def test_update_tag(self):
        tag = Tag.objects.create(name="After dinner", user=self.user)
        
        payload = {"name": "Dessert"}
        url = detail_url(tag_id=tag.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload["name"])

    def test_tag_delete(self):
        tag = Tag.objects.create(name="Test tag", user=self.user)
        url = detail_url(tag_id=tag.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tag = Tag.objects.filter(user=self.user)
        self.assertFalse(tag.exists())

   
       

