from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
import requests
from .serializers import UserSerializer, CameraSerializer
from rest_framework.pagination import LimitOffsetPagination

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 8

@api_view(['GET'])
def get_user_data(request):
    response = requests.get('https://jsonplaceholder.typicode.com/users').json()

    paginator = CustomLimitOffsetPagination()
    paginated_response = paginator.paginate_queryset(response, request)
    serializer = UserSerializer(paginated_response, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser]) # type: ignore
def post_user(request):
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
    data = request.data
    url = requests.post('https://jsonplaceholder.typicode.com/posts', json=data)
    response_data = url.json()
    serializer = UserSerializer(data=response_data)

    if serializer.is_valid():
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)
    
@api_view(['GET'])
def get_cameras(request):
    vendor_sid = 'root'
    vendor_key = 'Accelx123456'
    base_url = '192.168.1.13:8000'
    auth = (vendor_sid, vendor_key)

    headers = {
        'Content-type': 'Application/json'
    }
    api_url = f"http://{base_url}/camera/list"
    response = requests.get(api_url, auth=auth, headers=headers)

    
    cameras_data = response.json().get('cameras', [])
    paginator = CustomLimitOffsetPagination()
    paginated_response = paginator.paginate_queryset(cameras_data, request)
    serializer = CameraSerializer(paginated_response, many=True)
    return paginator.get_paginated_response(serializer.data)

