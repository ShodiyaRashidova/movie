import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponsePermanentRedirect
from django.utils.encoding import smart_str, \
    DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode

from rest_framework import status, serializers
from rest_framework.generics import CreateAPIView, RetrieveAPIView, \
    UpdateAPIView, GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .email import send_verify_email, send_reset_password
from .renderers import UserRenderer
from .serializers import RegisterSerializer, EmailVerificationSerializer, \
    LogInSerializer, PasswordUpdateSerializer, PasswordResetSerializer, \
    NewPasswordSerializer, LogoutSerizalizer


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = ['http', 'https']


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def perform_create(self, serializer):
        user = get_user_model().objects.create_user(**serializer.validated_data)
        send_verify_email(self.request, user)
        return user


class VerifyEmail(RetrieveAPIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request, *args, **kwargs):
        try:
            token = self.request.GET.get('token')
            user = get_user_model().objects.get_by_token(token)
            user.verify()
            return Response({'email': 'Successfully activated'},
                            status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'},
                            status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'},
                            status=status.HTTP_400_BAD_REQUEST)


class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer


class LogOutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerizalizer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token = RefreshToken(request.data["refresh_token"])
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserPasswordUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordUpdateSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user_model().objects.get(email=request.data.get('email'))
        send_reset_password(request, user)
        return Response(
            {'success': 'We have sent you a link to reset your password'},
            status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(GenericAPIView):
    def get(self, request, uidb64, token):
        redirect_url = request.GET.get('redirect_url')
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(id=user_id)
            if PasswordResetTokenGenerator().check_token(user, token):
                return CustomRedirect(redirect_url +
                                      '?token_valid=True&'
                                      'message=Credentials Valid&'
                                      'uidb64=' + uidb64 + '&token=' + token)
            return CustomRedirect(redirect_url + '?token_valid=False')
        except DjangoUnicodeDecodeError as identifier:
            return CustomRedirect(redirect_url + '?token_valid=False')


class SetNewPasswordAPIView(UpdateAPIView):
    serializer_class = NewPasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True,
                         'message': 'Password reset success'},
                        status=status.HTTP_200_OK)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "profile_image", "gender",
                  "date_of_birth")


class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
