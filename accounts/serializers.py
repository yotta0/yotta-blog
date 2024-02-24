from rest_framework import serializers
from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('This username already exists')

        return data

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'].lower()
        )
        user.set_password(validated_data['password'])

        return validated_data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):

        if not User.objects.filter(username=data['username'].lower()).exists():
            raise serializers.ValidationError('Account does not exist')

        return data

    def get_jwt_token(self, data):
        print(f'username: {data["username"]}, password: {data["password"]}')
        user = authenticate(username=data['username'].lower(), password=data['password'])

        if user is None:
            return {'message': 'Invalid credentials', 'data': None}

        refresh = RefreshToken.for_user(user)

        return {
            'message': 'login Successful',
            'data': {
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            }
        }
