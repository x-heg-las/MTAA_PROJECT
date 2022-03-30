import json, math
from django.http import JsonResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from django.http import FileResponse
from base.models import *
from django.db import IntegrityError
from . import util, validators
from django.db.models import Q
from django.core.exceptions import *
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.utils import timezone

#Fields
user_fields = ["id", "username", "profile_img_file", "user_type__name", "full_name", "phone_number", "created_at", "updated_at"]
request_fields = ["id", "title", "answered_by_user", "user", "request_type__name", "description", "call_requested", "file", "created_at", "updated_at"]

#Utility functions
def isAuthorized(header) -> bool:
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
            user_query = list(Users.objects.filter(id=request_params.get("id")).exclude(deleted_at__isnull=False).values(*user_fields))
            if len(user_query) != 0:
                return JsonResponse(user_query[0])
            else:
                return HttpResponseNotFound()
        for key in def_params:
            if request_params.get(key) != None:
                if type(def_params[key]) == int:
                    def_params[key] = int(request_params.get(key))
                else:
                    def_params[key] = request_params.get(key)
        if def_params["order_type"] == "DESC":
            def_params["order_by"] = ("-" + def_params["order_by"])
        start_from = ((def_params["page"] - 1) * def_params["per_page"])
        end_items = (def_params["page"] * def_params["per_page"])
        if def_params.get("query") != None:
            q &= Q(full_name__icontains=def_params.get("query"))
        user_count = Users.objects.all().filter(q).exclude(deleted_at__isnull=False).count()
        user_query = list(Users.objects.all().filter(q).exclude(deleted_at__isnull=False).order_by(def_params["order_by"])[start_from:end_items].values(*user_fields))
        user_meta = {"page": def_params["page"], "per_page": def_params["per_page"], "pages": math.ceil(user_count / def_params["per_page"]), "total": user_count}
        return JsonResponse({"items": user_query, "metadata": user_meta})
    elif request.method == "POST":
        try:
            if not request.body:
                return HttpResponse(status=422)
            request_body = json.loads(request.body)
            request_headers = request.headers
            result = validators.validateUserEntry(request_body)
            if not result["success"]:
                return JsonResponse({"errors": result["errors"]}, status=422)
            profile_image = None
            try:
                if request_body["profile_img_file"]:
                    profile_image = Files.objects.get(id=request_body["profile_img_file"])
            except ObjectDoesNotExist:
                profile_image = None
            new_user = Users(
                username=request_body["username"],
                profile_img_file=profile_image,
                user_type=UserTypes.objects.get(name=request_body["user_type__name"]),
                password=request_body["password"],
                full_name=request_body["full_name"],
                phone_number=request_body["phone_number"],
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            new_user.save()
            return JsonResponse(util.userToDictionary(new_user), status=201)
        except IntegrityError:
            return JsonResponse({"errors": {
                "reason": "Record already exists"
            }}, status=409)
    elif request.method == "PUT":
        if not request.body:
            return HttpResponse(status=422)
        try:
            params = request.GET.dict()
            request_body = json.loads(request.body)
            result = validators.validateUserEntry(request_body, updating=True)
            if not result["success"]:
                return JsonResponse({"errors": result["errors"]}, status=422)
            user_to_update = Users.objects.get(id=params.get("id"), deleted_at=None)
            for key, value in request_body.items():
                if key == "user_type__name":
                    util.update_model(user_to_update, "user_type", UserTypes.objects.get(name=value))
                    continue
                util.update_model(user_to_update, key, value)
            user_to_update.save()
            return JsonResponse(util.userToDictionary(user_to_update), status=200)
        except IntegrityError as ie:
            return JsonResponse({"errors": {"reason": "Integrity error"}}, status=422)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

    elif request.method == "DELETE":
        try:
            request_params = request.GET.dict()
            user_to_delete = Users.objects.exclude(deleted_at__isnull=False).get(id=request_params["id"])
            user_to_delete.deleted_at = timezone.now()
            user_to_delete.save()
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
            ticket_query = list(Requests.objects.filter(id=request_params.get("id")).exclude(deleted_at__isnull=False).values(*request_fields))
            if len(ticket_query) != 0:
                return JsonResponse(ticket_query[0])
            else:
                return HttpResponseNotFound()
        for key in def_params:
            if request_params.get(key) != None:
                if type(def_params[key]) == int:
                    def_params[key] = int(request_params.get(key))
                else:
                    def_params[key] = request_params.get(key)
        if def_params["order_type"] == "DESC":
            def_params["order_by"] = ("-" + def_params["order_by"])
        start_from = ((def_params["page"] - 1) * def_params["per_page"])
        end_items = (def_params["page"] * def_params["per_page"])
        if def_params.get("query") != None:
            q &= (Q(title__icontains=def_params.get("query")) | Q(description__icontains=def_params.get("query")))

        ticket_count = Requests.objects.all().filter(q).exclude(deleted_at__isnull=False).count()
        ticket_query = list(Requests.objects.all().filter(q).exclude(deleted_at__isnull=False).order_by(def_params["order_by"])[start_from:end_items].values(*request_fields))

        ticket_meta = {"page": def_params["page"], "per_page": def_params["per_page"], "pages": math.ceil(ticket_count / def_params["per_page"]), "total": ticket_count}
        return JsonResponse({"items": ticket_query, "metadata": ticket_meta})
    elif request.method == "POST":
        if not request.body:
            return HttpResponse(status=422)
        request_body = json.loads(request.body)
        result = validators.validateTicketEntry(request_body)
        if not result["success"]:
            return JsonResponse({"errors": result["errors"]}, status=422)
        appendix = None
        if request_body.get("file"):
            appendix = Files.objects.get(id=request_body["file"])
        new_ticket = Requests(
            title=request_body["title"],
            user_id=request_body["user"],
            request_type_id=RequestTypes.objects.filter(name=request_body["request_type__name"]).values("id")[0]["id"],
            file=appendix,
            description=request_body["description"],
            call_requested=request_body["call_requested"],
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        new_ticket.save()
        return JsonResponse(util.requestToDictionary(new_ticket), status=201)

    elif request.method == "PUT":
        try:
            if not request.body:
                return JsonResponse({"errors": "No request body provided"}, status=422)
            request_body = json.loads(request.body)
            request_params = request.GET.dict()
            result = validators.validateTicketEntry(request_body, updating=True)
            if not result["success"]:
                return JsonResponse({"errors": result["errors"]}, status=422)
            updated_ticket = Requests.objects.get(id=request_params["id"])
            for key, value in request_body.items():
                if key == "request_type__name":
                    util.update_model(updated_ticket, "request_type", RequestTypes.objects.get(name=value))
                    continue
                if key == "user":
                    util.update_model(updated_ticket, "user", Users.objects.get(id=value))
                    continue
                if key == "answered_by_user":
                    util.update_model(updated_ticket, "answered_by_user", Users.objects.get(id=value))
                    continue
                util.update_model(updated_ticket, key, value)
            updated_ticket.save()
            return JsonResponse(util.requestToDictionary(updated_ticket))
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
    elif request.method == "DELETE":
        try:
            ticket_param = request.GET.get("id")
            ticket_query = Requests.objects.exclude(deleted_at__isnull=False).get(id=ticket_param)
            ticket_query.deleted_at = timezone.now()
            ticket_query.save()
            return HttpResponse(status=204)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
    else:
        return HttpResponseNotFound()

@csrf_exempt
def responsePostFile(request, *args, **kwargs):
    if not isAuthorized(request.headers):
        return HttpResponse('Unauthorized', status=401)
    if request.method == "POST":
        file_name = kwargs.get("fileName")
        fileExt = file_name.split(".")[-1]
        new_file = Files(
            file_type=FileTypes.objects.get(name=fileExt),
            data=ContentFile(request.body, name=file_name),
            size=len(request.body),
            created_at=timezone.now(),
            updated_at=timezone.now())
        new_file.save()
        return JsonResponse(util.fileToDictionary(new_file), status=201)
    else:
        return HttpResponseNotFound()

def responseGetFile(request, *args, **kwargs):
    if not isAuthorized(request.headers):
        return HttpResponse('Unauthorized', status=401)
    if request.method == "GET":
        q = Q()
        def_params = {"query": None}
        request_params = request.GET.dict()
        if request_params.get("id") != None:
            file_query = Files.objects.filter(id=request_params.get("id")).get()
            return FileResponse(open(file_query.data.path, "rb"))
        for key in def_params:
            if request_params.get(key) != None:
                def_params[key] = request_params.get(key)
        if def_params.get("query") != None:
            q &= Q(data__icontains=def_params.get("query"))
        file_entry = Files.objects.filter(q).order_by("id").all()
        if len(file_entry) == 0:
            return HttpResponseNotFound()
        return FileResponse(open(file_entry[0].data.path, "rb"))
    else:
        return HttpResponseNotFound()
