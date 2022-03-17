import django, json
from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseForbidden
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
def getUsers(request, *args, **kwargs):
    if request.method == "GET":
        if not isAuthorized(request.headers):
            return HttpResponseForbidden()
        return JsonResponse({}, safe=False)
    else:
        return HttpResponseNotFound()
