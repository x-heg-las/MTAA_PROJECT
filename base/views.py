import json, math
from django.http import JsonResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from base.models import *
from . import util, validators
from django.db.models import Q
from django.core import serializers
from django.core.exceptions import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

#Fields
user_fields = ["id", "username", "profile_img_file__data", "user_type__name", "full_name", "phone_number", "created_at", "updated_at"]
request_fields = ["id", "title", "answered_by_user__username", "user__username", "request_type__name", "description", "call_requested", "file__data", "created_at", "updated_at"]

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
    if not isAuthorized(request.headers):
        return HttpResponse('Unauthorized', status=401)
    if request.method == "GET":
        user_query = None
        q = Q()
        def_params = {"page": 1, "per_page": 5, "order_by": "id", "order_type": "ASC", "query": None}
        request_params = request.GET.dict()
        if request_params.get("id") != None:
            user_query = list(Users.objects.filter(id=request_params.get("id")).values(*user_fields))
            if len(user_query) != 0:
                return JsonResponse(user_query[0])
            else:
                return JsonResponse({})
        for key in def_params:
            if request_params.get(key) != None:
                if type(def_params[key]) == int:
                    def_params[key] = int(request_params.get(key))
                else:
                    def_params[key] = request_params.get(key)
        if def_params["order_type"] == "DESC":
            def_params["order_by"] = ("-" + def_params["order_by"])
        start_from = ((def_params["page"] - 1) * def_params["per_page"])
        if def_params.get("query") != None:
            q &= Q(full_name__icontains=def_params.get("query"))
        user_count = Users.objects.all().filter(q).count()
        user_query = list(Users.objects.all().filter(q).order_by(def_params["order_by"])[start_from:def_params["per_page"]].values(*user_fields))
        user_meta = {"page": def_params["page"], "per_page": def_params["per_page"], "pages": math.ceil(user_count / def_params["per_page"]), "total": user_count}
        return JsonResponse({"items": user_query, "metadata": user_meta})
    elif request.method == "POST":
        pass
    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        try:
            request_params = request.GET.dict()
            user_to_delete = Users.objects.get(request_params["id"])
            user_to_delete.delete()
            return HttpResponse(status=204)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
    else:
        return HttpResponseNotFound()

@csrf_exempt
def responseTickets(request, *args, **kwargs):
    if not isAuthorized(request.headers):
        return HttpResponse('Unauthorized', status=401)
    if request.method == "GET":
        ticket_query = None
        q = Q()
        def_params = {"page": 1, "per_page": 5, "order_by": "id", "order_type": "ASC", "query": None}
        request_params = request.GET.dict()
        if request_params.get("id") != None:
            ticket_query = list(Requests.objects.filter(id=request_params.get("id")).values(*request_fields))
            if len(ticket_query) != 0:
                return JsonResponse(ticket_query[0])
            else:
                return JsonResponse({})
        for key in def_params:
            if request_params.get(key) != None:
                if type(def_params[key]) == int:
                    def_params[key] = int(request_params.get(key))
                else:
                    def_params[key] = request_params.get(key)
        if def_params["order_type"] == "DESC":
            def_params["order_by"] = ("-" + def_params["order_by"])
        start_from = ((def_params["page"] - 1) * def_params["per_page"])
        if def_params.get("query") != None:
            q &= Q(title__icontains=def_params.get("query"))
        ticket_count = Requests.objects.all().filter(q).count()
        ticket_query = list(Requests.objects.all().filter(q).order_by(def_params["order_by"])[start_from:def_params["per_page"]].values(*request_fields))
        ticket_meta = {"page": def_params["page"], "per_page": def_params["per_page"], "pages": math.ceil(ticket_count / def_params["per_page"]), "total": ticket_count}
        return JsonResponse({"items": ticket_query, "metadata": ticket_meta})
    elif request.method == "POST":
        if not request.body:
            return HttpResponse(status=422)
        request_body = json.loads(request.body)
        result = validators.validateTicketEntry(request_body)
        if not result["success"]:
            return JsonResponse({"errors": result["errors"]}, status=422)

        new_ticket = Requests(
            title=request_body["title"],
            user_id=request_body["user_id"],
            request_type_id=request_body["request_type_id"],
            #file=Files.get(id=request_body["file_id"]),
            description=request_body["description"],
            call_requested=request_body["call_requested"],
            created_at=datetime.now()
        )
        new_ticket.save()
        return JsonResponse(util.requestToDictionary(new_ticket))

    elif request.method == "PUT":
        try:
            if not request.body:
                return HttpResponse(status=422)
            request_body = json.loads(request.body)
            request_params = request.GET.dict()
            result = validators.validateTicketEntry(request_body, True)

            if not result["success"]:
                return JsonResponse({"errors": result["errors"]}, status=422)

            updated_ticket = Requests.objects.get(id=request_params["id"])
            for key, value in request_body.items():
                util.update_model(updated_ticket, key, value)
                updated_ticket.save()
            return JsonResponse(util.requestToDictionary(updated_ticket))
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
    elif request.method == "DELETE":
        try:
            ticket_param = request.GET.get("id")
            ticket_query = Requests.objects.get(id=ticket_param)
            ticket_query.delete()
            return HttpResponse(status=204)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
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
