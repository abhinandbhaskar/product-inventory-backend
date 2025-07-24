from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not user:
            raise AuthenticationFailed("User not registered or invalid credentials")
        if not user.is_active:
            raise AuthenticationFailed("This account is disabled. Please contact support.")
        
        if not hasattr(user, 'userprofile') or not user.userprofile.is_admin:
            raise AuthenticationFailed("Only admins can log in here.")

        if user.is_superuser:
            raise AuthenticationFailed("Superusers are not allowed to login here.")

        data["user_id"] = user.id
        data["username"] = user.username
        data["email"] = user.email

        return data
