from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.urls import path
from . import views
urlpatterns = [
    path('users/login/', TokenObtainPairView.as_view(), name='user_login'),
    path('get-data/', views.get_user_data, name="get_user_data"),
    path('create/', views.post_user, name='create_user'),
    path('cameras/', views.get_cameras, name="get_cameras"),
]