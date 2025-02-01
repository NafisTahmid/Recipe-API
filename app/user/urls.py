"""
URLs mapping for the user
"""
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    # path('users/login/', TokenObtainPairView.as_view(), name='user_login'),
    path('create/', views.CreateUserView.as_view(), name="create"),
    path('token/', views.CreateTokenView.as_view(), name="token"),
    path('me/', views.ManageUserView.as_view(), name="me")
    # path('get-data/', views.get_user_data, name="get_user_data"),
    # path('create-post/', views.post_user, name='create_post')
]