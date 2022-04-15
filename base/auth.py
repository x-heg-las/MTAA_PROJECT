from django.contrib.auth.backends import BaseBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from base.models import Users
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings
from django.db.models import BooleanField, Value
from rest_framework.permissions import BasePermission

def authRule(user):
    return user is not None

class UsersBackend(BaseBackend):
    def get_user(self, user_id):
        userObj = Users.objects.filter(id=user_id).annotate(is_authenticated=Value(True, output_field=BooleanField()))\
            .annotate(is_active=Value(True, output_field=BooleanField())).first()
        return userObj

    def authenticate(self, request, username=None, password=None):
        user = Users.objects.filter(username=username).annotate(is_authenticated=Value(True, output_field=BooleanField()))\
            .annotate(is_active=Value(True, output_field=BooleanField())).first()
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

class CustomIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user)
