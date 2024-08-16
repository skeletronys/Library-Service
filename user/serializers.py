from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError("Username already exists.")
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        password = validated_data.get("password", None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
