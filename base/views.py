from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse

# Create your views here.
def getUsers(request):
    return JsonResponse({"results" : "pouzivatelia"}, safe=False)