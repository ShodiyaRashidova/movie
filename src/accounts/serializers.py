from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=555)

class LogInSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not self.user.is_verified:
            raise exceptions.AuthenticationFailed(
                "Activate your account by Email to Login"
            )
        attrs["is_staff"] = self.user.is_staff
        return attrs


class PasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                'Your old password was entered incorrectly. '
            )
        return value

    def validate(self, attrs):
        new_password = attrs["new_password"]
        confirm_password = attrs["confirm_password"]
        if new_password != confirm_password:
            raise serializers.ValidationError("passwords do not match")
        return attrs

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    redirect_url = serializers.CharField(max_length=500)

    def validate(self, attrs):
        if not get_user_model().objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("This Email does not exist")
        return attrs


class NewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    def validate(self, attrs):
        try:
            user_id = force_str(urlsafe_base64_decode(attrs["uidb64"]))
            user = get_user_model().objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user,
                                                             attrs["token"]):
                raise AuthenticationFailed('The reset link is invalid', 401)
            user.set_password(attrs["password"])
            user.is_verified = True
            user.save()
            return attrs
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)


class LogoutSerizalizer(serializers.Serializer):
    refresh = serializers.CharField(max_length=555)
