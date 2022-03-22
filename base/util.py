def requestToDictionary(request):
    output = {"id": request.id, "title": request.title, "user_id": request.user.id,
              "request_type_id": request.request_type.id, "description": request.description,
              "call_reqested": request.call_requested, "created_at": request.created_at,
              "updated_at": request.updated_at}
    return output


def update_model(self, key, value):
    getattr(self, key)
    setattr(self, key, value)
