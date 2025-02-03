from core.models import (
    Recipe,
    Tag)
from django.contrib.auth import get_user_model

from rest_framework import serializers
from user.serializers import UserSerializer 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'name'] 

class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag view"""
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

    def create(self,validated_data):
        """Create a recipe"""
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)
        return recipe
    

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for Recipe Detail view"""
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']

