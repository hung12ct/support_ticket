from django.urls import path, include
from .apiaccounts import UserCreate
# from rest_framework_simplejwt import views as jwt_views
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.views import LogoutView, LoginView
from . import views

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('settings/', views.UserUpdateView.as_view(), name='my_account'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'),
         name='login'),
    path('api/signup/', UserCreate.as_view(), name='account_create'),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    #     path('api/token/', jwt_views.TokenObtainPairView.as_view(),
    #          name='token_obtain_pair'),
    #     path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(),
    #          name='token_refresh'),
]
