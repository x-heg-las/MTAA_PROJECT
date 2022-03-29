from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from base.models import UserTypes, FileTypes, RequestTypes
from base.util import typeToDictionary


@csrf_exempt
def userTypes(request, *args, **kwargs):
    types = list(UserTypes.objects.all())
    response = list()
    for type in types:
        response.append(typeToDictionary(type))
    return JsonResponse({"items": response})


@csrf_exempt
def fileTypes(request, *args, **kwargs):
    types = FileTypes.objects.all()
    response = list()
    for type in types:
        response.append(typeToDictionary(type))
    return JsonResponse({"items": response})


@csrf_exempt
def requestTypes(request, *args, **kwargs):
    types = RequestTypes.objects.all()
    response = list()
    for type in types:
        response.append(typeToDictionary(type))
    return JsonResponse({"items": response})