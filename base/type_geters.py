from rest_framework.response import Response
from rest_framework.views import APIView
from base.auth import CustomIsAuthenticated
from base.models import UserTypes, FileTypes, RequestTypes
from base.util import typeToDictionary

class UserTypes(APIView):
    permission_classes = (CustomIsAuthenticated,)

    def get(self, request, *args, **kwargs):
        types = list(UserTypes.objects.all())
        response = list()
        for type in types:
            response.append(typeToDictionary(type))
        return Response({"items": response})

class FileTypes(APIView):
    permission_classes = (CustomIsAuthenticated,)

    def get(request, *args, **kwargs):
        types = FileTypes.objects.all()
        response = list()
        for type in types:
            response.append(typeToDictionary(type))
        return Response({"items": response})

class RequestTypes(APIView):
    permission_classes = (CustomIsAuthenticated,)

    def get(request, *args, **kwargs):
        types = RequestTypes.objects.all()
        response = list()
        for type in types:
            response.append(typeToDictionary(type))
        return Response({"items": response})
