from django.contrib.auth import get_user_model
from rest_framework import serializers

from rest_framework.authtoken.serializers import AuthTokenSerializer as BaseAuthTokenSerializer


class AuthTokenSerializer(BaseAuthTokenSerializer):
    username_field = "email"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "is_staff")
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            username=validated_data.get("username")
        )

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user
