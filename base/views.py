import json
from django.http import JsonResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from base.models import *
from django.views.decorators.csrf import csrf_exempt

#Utility functions
def isAuthorized(header):
    """
    Function to check if user is authorized.\n
    Returns True if user is authorized.\n
    Returns False if user is unauthorized.
    """
    if ("username" in header) and ("password" in header):
        request_headers = {"username": header["username"], "password": header["password"]}
        user = list(Users.objects.filter(username=request_headers["username"]).values())
        if len(user) == 0:
            return False
        if user[0]["password"] == request_headers["password"]:
            return True
    return False

# Create your views here.
@csrf_exempt
def postLogin(request, *args, **kwargs):
    if request.method == "POST":
        data = json.loads(request.body)
        user_data = list(Users.objects.filter(username=data["username"]).values())
        if (len(user_data) == 0) or (user_data[0]["password"] != data["password"]):
            return HttpResponse('Unauthorized', status=401)
        del user_data[0]["password"]
        del user_data[0]["deleted_at"]
        return JsonResponse(user_data[0])
    else:
        return HttpResponseNotFound()

@csrf_exempt
def responseUsers(request, *args, **kwargs):
    if request.method == "GET":
        if not isAuthorized(request.headers):
            return HttpResponse('Unauthorized', status=401)
        return JsonResponse({})
    elif request.method == "POST":
        pass
    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
    else:
        return HttpResponseNotFound()

@csrf_exempt
def responseTickets(request, *args, **kwargs):
    if request.method == "GET":
        if not isAuthorized(request.headers):
            return HttpResponse('Unauthorized', status=401)
        return JsonResponse({})
    elif request.method == "POST":
        pass
    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
    else:
        return HttpResponseNotFound()

@csrf_exempt
def responseFile(request, *args, **kwargs):
    if request.method == "GET":
        if not isAuthorized(request.headers):
            return HttpResponse('Unauthorized', status=401)
        return JsonResponse({})
    elif request.method == "POST":
        pass
    else:
        return HttpResponseNotFound()
