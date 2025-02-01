"""
Views for the user API
"""
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import generics,authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.pagination import LimitOffsetPagination
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer
    )

# Create your views here.
class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 8

class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the system """
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

# @api_view(['GET'])
# def get_user_data(request):
#     response = requests.get('https://jsonplaceholder.typicode.com/users').json()

#     paginator = CustomLimitOffsetPagination()
#     paginated_response = paginator.paginate_queryset(response, request)
#     serializer = UserSerializer(paginated_response, many=True)
#     return paginator.get_paginated_response(serializer.data)

# @api_view(['POST'])
# @permission_classes([IsAdminUser]) # type: ignore
# def post_user(request):
    # name = 'test user'
    # username = 'testuser'
    # email = 'test@beet.com'
    # address = {
    #     'street':'Demo street',
    #     'suite': 'Demo suite',
    #     'city': 'Unknown city',
    #     'zipcode': 'xxxx-1234',
    #     'geo': {
    #         'lat': 'test lat',
    #         'lng': 'test lng'
    #     }
    # }
    # phone = 'demo-phone'
    # website = 'demo-website'
    # company = {
    #     'name': 'Demo company',
    #     'catchPhrase': 'test phrase',
    #     'bs': 'test bs'
    # }

    # demo_user = {
     
    #     'name':name,
    #     'username':username,
    #     'email':email,
    #     'address':address,
    #     'phone':phone,
    #     'website':website,
    #     'company':company
    # }
    # data = request.data
    # url = requests.post('https://jsonplaceholder.typicode.com/posts', json=data)
    # response_data = url.json()
    # serializer = UserSerializer(data=response_data)

    # if serializer.is_valid():
    #     return Response(serializer.data)
    # else:
    #     return Response(serializer.errors, status=400)

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Return and retrieve the authenticated user."""
        return self.request.user
