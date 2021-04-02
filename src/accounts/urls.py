from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import RegisterView, VerifyEmail, LogInView, LogOutView, \
    UserPasswordUpdateView, PasswordResetView, PasswordTokenCheckAPI, \
    SetNewPasswordAPIView, UserProfileView, AdminListUserView, \
    UpdateUserStatusView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LogInView.as_view(), name="login"),
    path('logout/', LogOutView.as_view(), name="logout"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password/update/', UserPasswordUpdateView.as_view(),
         name='update_password'),

    path('password-reset/', PasswordResetView.as_view(),
         name="password-reset"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('profile/', UserProfileView.as_view(), name="email-verify"),
    path('users/', AdminListUserView.as_view(), name="user_list"),
    path("users/<uuid:guid>/", UpdateUserStatusView.as_view(),
         name="user_list"),

]
