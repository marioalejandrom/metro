from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('profile/', views.ManageUserView.as_view(), name='profile')
]
