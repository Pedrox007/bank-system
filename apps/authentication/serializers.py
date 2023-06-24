from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from typing import cast

from authentication.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(
        min_length=4, max_length=255, required=True)
    first_name = serializers.CharField(
        min_length=1, max_length=255, required=True)
    last_name = serializers.CharField(
        min_length=1, max_length=255, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        max_length=255, required=True, write_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'email', 'password', 'created_at')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]

    def create(self, validated_data: dict):
        password: str = cast(str, validated_data.get('password'))
        print('@' * 2000)
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def update(self, instance: User, validated_data: dict):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        return instance
