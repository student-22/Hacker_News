from django.contrib.auth.models import User
from rest_framework import serializers, validators


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        min_length=5,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True, validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        password = attrs["password"]
        confirm_password = attrs["confirm_password"]

        if password != confirm_password:
            raise serializers.ValidationError(detail="password does not match", code="password_match")

        return attrs

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
