from rest_framework import serializers
from users.models import Account
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'bio', 'first_name', 'last_name', 'password']
        read_only_fields = ['id']

    def validate_password(self, value):
        """
        Ensure the password meets Django's validation criteria.
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Account.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
