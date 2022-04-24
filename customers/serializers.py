from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Leave empty if no change needed",
        style={"input_type": "password", "placeholder": "Password"},
    )

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(UserSerializer, self).create(validated_data)

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "password")


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username",)

    def validate_username(self, value):
        try:
            User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                f"There's no user with the username '{value}'. Please register first."
            )
        return value
