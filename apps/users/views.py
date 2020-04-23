from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.models import User


def auth_details(user: User):
    details = {'is_authenticated': user.is_authenticated}
    if user.is_authenticated:
        details['email'] = user.email

    return details


class StatusView(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):  # noqa: WPS125
        return Response(auth_details(request.user))


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': 'Invalid username or password'
    }

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['exp_refresh'] = refresh.get('exp')
        data['exp_access'] = refresh.access_token.get('exp')

        return data


class CustomRefreshTokenSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        data = {
            'access': str(refresh.access_token),
            'exp_access': refresh.access_token.get('exp')
        }

        refresh.set_jti()
        refresh.set_exp()

        data['refresh'] = str(refresh)
        data['exp_refresh'] = refresh.get('exp')

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomRefreshTokenSerializer
