"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core import models 
from django.contrib.auth import get_user_model

def create_user():
    return get_user_model().objects.create_user(
        email="test@example.com",
        password="test@123"
    )

class ModelTest(TestCase):
    def test_create_user_with_email_successful(self):
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_create_super_user(self):
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_recipe_api(self):
        """Test creating a new recipe api"""
        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="test@1234"
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title="Demo title",
            time_minutes = 5,
            price=Decimal('5.5'),
            description = 'Test recipe'
        )
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        user = create_user()
        tag = models.Tag.objects.create(
            user=user,
            name="Test tag"
        )
        self.assertEqual(str(tag), tag.name)