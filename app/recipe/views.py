from django.shortcuts import render
from rest_framework import (viewsets,
                             mixins
                            )
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import (Recipe, Tag)
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer, TagSerializer

"""Views for recipe"""
# Create your views here.
class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id') 
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeSerializer
        return self.serializer_class
    
    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

class TagViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
      ):
    """Viewset for listing tags filtered by authenticated user."""
    serializer_class = TagSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return tags for the authenticated user only."""
        return Tag.objects.filter(user=self.request.user).order_by('-name')