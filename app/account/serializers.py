from rest_framework import serializers
import string
import random

from .models import LoginCodeEmail


class LoginEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = LoginCodeEmail
        fields = ('email',)

    def validate_email(self, value):
        return value.lower()

    def create(self, validated_data):
        email = validated_data['email']
        code = ''.join(random.choice(string.digits) for _ in range(4))
        return LoginCodeEmail.objects.create(
            email=email,
            code=code,
        )


class LoginEmailCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)
    email = serializers.EmailField()

    def validate_email(self, value):
        return value.lower()

    def create(self, validated_data):
        email = validated_data.get('email')
        code = validated_data.get('code')
        login_code = LoginCodeEmail.objects.filter(email=email, code=code)
        if not login_code.exists():
            raise serializers.ValidationError({'code': ['Введен неверный код']})
        return email
