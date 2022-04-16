from django.contrib.auth.backends import BaseBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from base.models import Users
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework.permissions import IsAuthenticated

def authRule(user):
    return user is not None

class UsersBackend(BaseBackend):
    def get_user(self, user_id):
        userObj = Users.objects.filter(id=user_id).first()
        return userObj

    def authenticate(self, request, username=None, password=None):
        user = Users.objects.filter(username=username).first()
        if user == None:
            return None
        if user.password == password:
            return user
        return None

class CustomJWT(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = Users
    
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable user identification"))

        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed(_("User not found"), code="user_not_found")

        return user

class CustomIsAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        token_exists = True
        if "Authorization" not in request.headers:
            token_exists = False
        return bool(request.user and token_exists)
