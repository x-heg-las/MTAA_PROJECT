import json, math
from django.http import FileResponse
from base.models import *
from django.db import IntegrityError
from . import util, validators
from django.db.models import Q
from django.core.exceptions import *
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from base.auth import CustomIsAuthenticated

#Fields
user_fields = ["id", "username", "profile_img_file", "user_type__name", "full_name", "phone_number", "created_at", "updated_at"]
request_fields = ["id", "title", "answered_by_user", "answer", "user", "request_type__name", "description", "call_requested", "file", "created_at", "updated_at"]

# Create your views here.

class UsersView(APIView):
    permission_classes = (CustomIsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            user_query = None
            q = Q()
            def_params = {"page": 1, "per_page": -1, "order_by": "id", "order_type": "ASC", "query": None, "username": None}
            request_params = request.GET.dict()
            if request_params.get("id") != None:
                user_query = list(Users.objects.filter(id=request_params.get("id")).exclude(deleted_at__isnull=False).values(*user_fields))
                if len(user_query) != 0:
                    return Response(user_query[0])
                else:
                    return Response(status=404)
            for key in def_params:
                if request_params.get(key) != None:
                    if type(def_params[key]) == int:
                        def_params[key] = int(request_params.get(key))
                    else:
                        def_params[key] = request_params.get(key)
            if def_params["order_type"] == "DESC":
                def_params["order_by"] = ("-" + def_params["order_by"])
            if def_params.get("query") != None:
                q &= Q(full_name__icontains=def_params.get("query"))
            if def_params.get("username") != None:
                q &= Q(username=def_params.get("username"))
            user_count = Users.objects.all().filter(q).exclude(deleted_at__isnull=False).count()
            if (def_params["per_page"] == -1):
                user_query = list(Users.objects.all().filter(q).exclude(deleted_at__isnull=False).order_by(def_params["order_by"]).values(*user_fields))
                user_meta = {"total": user_count}
                return Response({"items": user_query, "metadata": user_meta})
            else:
                start_from = ((def_params["page"] - 1) * def_params["per_page"])
                end_items = (def_params["page"] * def_params["per_page"])
                user_query = list(Users.objects.all().filter(q).exclude(deleted_at__isnull=False).order_by(def_params["order_by"])[start_from:end_items].values(*user_fields))
                user_meta = {"page": def_params["page"], "per_page": def_params["per_page"], "pages": math.ceil(user_count / def_params["per_page"]), "total": user_count}
                return Response({"items": user_query, "metadata": user_meta})
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            if not request.body:
                return Response(status=422)
            request_body = json.loads(request.body)
            request_headers = request.headers
            result = validators.validateUserEntry(request_body)
            if not result["success"]:
                return Response({"errors": result["errors"]}, status=422)
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
            return Response(util.userToDictionary(new_user), status=201)
        except IntegrityError:
            return Response({"errors": {
                "reason": "Record already exists"
            }}, status=409)

    @csrf_exempt
    def put(self, request, *args, **kwargs):
        if not request.body:
            return Response(status=422)
        try:
            params = request.GET.dict()
            request_body = json.loads(request.body)
            result = validators.validateUserEntry(request_body, updating=True)
            if not result["success"]:
                return Response({"errors": result["errors"]}, status=422)
            user_to_update = Users.objects.get(id=params.get("id"), deleted_at=None)
            for key, value in request_body.items():
                if key == "user_type__name":
                    util.update_model(user_to_update, "user_type", UserTypes.objects.get(name=value))
                    continue
                util.update_model(user_to_update, key, value)
            user_to_update.save()
            return Response(util.userToDictionary(user_to_update), status=200)
        except IntegrityError as ie:
            return Response({"errors": {"reason": "Integrity error"}}, status=422)
        except ObjectDoesNotExist:
            return Response(status=404)

    def delete(self, request, *args, **kwargs):
        try:
            request_params = request.GET.dict()
            user_to_delete = Users.objects.exclude(deleted_at__isnull=False).get(id=request_params["id"])
            user_to_delete.deleted_at = timezone.now()
            user_to_delete.save()
            return Response(status=204)
        except ObjectDoesNotExist:
            return Response(status=404)

class TicketsView(APIView):
    permission_classes = (CustomIsAuthenticated,)

    def get(self, request, *args, **kwargs):
        ticket_query = None
        q = Q()
        def_params = {"page": 1, "per_page": -1, "order_by": "id", "order_type": "ASC", "query": None, "status": None, "user_id": None}
        request_params = request.GET.dict()
        if request_params.get("id") != None:
            ticket_query = list(Requests.objects.filter(id=request_params.get("id")).exclude(deleted_at__isnull=False).values(*request_fields))
            if len(ticket_query) != 0:
                return Response(ticket_query[0])
            else:
                return Response(status=404)
        for key in def_params:
            if request_params.get(key) != None:
                if type(def_params[key]) == int:
                    def_params[key] = int(request_params.get(key))
                else:
                    def_params[key] = request_params.get(key)
        if def_params["order_type"] == "DESC":
            def_params["order_by"] = ("-" + def_params["order_by"])
        if def_params.get("query") != None:
            q &= (Q(title__icontains=def_params.get("query")) | Q(description__icontains=def_params.get("query")))
        if def_params.get("status") != None:
            q &= Q(request_type__name=def_params.get("status"))
        if def_params.get("user_id") != None:
            q &= Q(user__id=int(def_params.get("user_id")))
        ticket_count = Requests.objects.all().filter(q).exclude(deleted_at__isnull=False).count()
        if (def_params["per_page"] == -1):
            ticket_query = list(Requests.objects.all().filter(q).exclude(deleted_at__isnull=False).order_by(def_params["order_by"]).values(*request_fields))
            ticket_meta = {"total": ticket_count}
            return Response({"items": ticket_query, "metadata": ticket_meta})
        else:
            start_from = ((def_params["page"] - 1) * def_params["per_page"])
            end_items = (def_params["page"] * def_params["per_page"])
            ticket_query = list(Requests.objects.all().filter(q).exclude(deleted_at__isnull=False).order_by(def_params["order_by"])[start_from:end_items].values(*request_fields))
            ticket_meta = {"page": def_params["page"], "per_page": def_params["per_page"], "pages": math.ceil(ticket_count / def_params["per_page"]), "total": ticket_count}
            return Response({"items": ticket_query, "metadata": ticket_meta})
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if not request.body:
            return Response(status=422)
        request_body = json.loads(request.body)
        result = validators.validateTicketEntry(request_body)
        if not result["success"]:
            return Response({"errors": result["errors"]}, status=422)
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
        return Response(util.requestToDictionary(new_ticket), status=201)
    
    @csrf_exempt
    def put(self, request, *args, **kwargs):
        try:
            if not request.body:
                return Response({"errors": "No request body provided"}, status=422)
            request_body = json.loads(request.body)
            request_params = request.GET.dict()
            result = validators.validateTicketEntry(request_body, updating=True)
            if not result["success"]:
                return Response({"errors": result["errors"]}, status=422)
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
            return Response(util.requestToDictionary(updated_ticket))
        except ObjectDoesNotExist:
            return Response(status=404)
    
    def delete(self, request, *args, **kwargs):
        try:
            ticket_param = request.GET.get("id")
            ticket_query = Requests.objects.exclude(deleted_at__isnull=False).get(id=ticket_param)
            ticket_query.deleted_at = timezone.now()
            ticket_query.save()
            return Response(status=204)
        except ObjectDoesNotExist:
            return Response(status=404)

class FilePostView(APIView):
    permission_classes = (CustomIsAuthenticated,)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        file_name = kwargs.get("fileName")
        fileExt = file_name.split(".")[-1]
        new_file = Files(
            file_type=FileTypes.objects.get(name=fileExt),
            data=ContentFile(request.body, name=file_name),
            size=len(request.body),
            created_at=timezone.now(),
            updated_at=timezone.now())
        new_file.save()
        return Response(util.fileToDictionary(new_file), status=201)

class FileGetView(APIView):
    permission_classes = (CustomIsAuthenticated,)

    def get(self, request, *args, **kwargs):
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
            return Response(status=404)
        return Response(open(file_entry[0].data.path, "rb"))
