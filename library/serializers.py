from django.db import IntegrityError
from rest_framework import serializers

from library.models import Book, Customer


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(required=False)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = Customer
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_staff",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        try:
            user = Customer.objects.create_user(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError("Username already exists.")
        return user

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if request and not request.user.is_staff:
            raise serializers.PermissionDenied(
                "You do not have permission to update user admin status."
            )

        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.is_staff = validated_data.get("is_staff", instance.is_staff)

        password = validated_data.get("password", None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
