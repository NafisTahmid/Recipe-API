from django.test import TestCase
from rest_framework.test import APIClient
from core.models import Recipe
from decimal import Decimal
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id])

def create_recipe(user, **params):
    defaults = {
        'title': 'Test title',
        'description': 'Test description',
        'time_minutes': 4,
        'price': Decimal('5.5'),
        'link': 'demo.pdf'
    }
    defaults.update(params)
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicRecipeAPITests(TestCase):
    """Test unauthenticated api uses"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeAPITests(TestCase):
    """Test authenticated API uses"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email="test@example.com",
            password="test@1234"
        )
        self.client.force_authenticate(self.user)

    

    def test_retrieve_recipes(self):
        """Test retrieve recipes for authenticated users"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)
        res = self.client.get(RECIPES_URL)
        recipes =Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_recipe_list_to_limited_user(self):
        """Testing authenticated users sorted recipes to all recipes"""
        other_user = create_user(
            email="other@example.com",
            password="test@123"
        )
        
        create_recipe(user=other_user)
        create_recipe(user=self.user)
        res = self.client.get(RECIPES_URL)
        data = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(data, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.data, serializer.data)

    def test_get_recipe_details(self):
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe, many=False)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test successfully create a recipe"""
        payload = {
            'title': "Test title",
            'time_minutes': 4,
            'price': Decimal('3.99')
        }
        res = self.client.post(RECIPES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
        """Check partial update or a recipe"""
        original_link="http://www.example.com"
        recipe = create_recipe(
            user=self.user,
            title="test title",
            link=original_link

        )
        url = detail_url(recipe.id)
        payload = {
            'title':'Updated title'
        }
        res = self.client.patch(url, payload)
        recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)

    def test_full_update(self):
        """Full update of a recipe"""
        recipe = create_recipe(
            user=self.user,
            title="Test title",
            link="http://testlink.com"
        )
        payload = {
            'title':'Updated title',
            'description':'Test description',
            'time_minutes': 10,
            'price': Decimal('5.5'),
            'link': 'http://updatedtestlink.com'
        }
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)
        recipe.refresh_from_db()
        for k,v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)
    
    def test_update_user_returns_error(self):
        new_user = create_user(email="new_user@example.com", password="test@123")
        recipe = create_recipe(user=self.user)
        payload = {
            'user': new_user.id
        }
        url = detail_url(recipe.id)

        res = self.client.patch(url, payload)
        recipe.refresh_from_db()
        # self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(recipe.user, self.user)
    
    def test_delete_recipe(self):
        """Test deleting a recipe successful"""
        recipe = create_recipe(user=self.user)
        retrieved_recipe = detail_url(recipe.id)
        res = self.client.delete(retrieved_recipe)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_delete_recipe_other_user_recipe_error(self):
        """Test deleting other user's recipe error"""
        new_user = create_user(
            email="new_user@example.com",
            password="test@1234"
        )
        recipe = create_recipe(user=new_user)
        url = detail_url(recipe.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())
