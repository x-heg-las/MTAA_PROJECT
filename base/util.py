def requestToDictionary(request) ->dict:
    output = {"id": request.id, "title": request.title, "user": request.user.id, "answered_by_user": request.answered_by_user,
              "request_type__name": request.request_type.name, "description": request.description,
              "call_reqested": request.call_requested, "file": request.file, "created_at": request.created_at,
              "updated_at": request.updated_at}
    return output


def userToDictionary(user) ->dict:
    output = {"id": user.id, "username": user.username, "user_type__name": user.user_type.name,
              "full_name": user.full_name, "phone_number": user.phone_number, "created_at": user.created_at,
              "updated_at": user.updated_at}
    if user.profile_img_file:
        output["profile_img_file"] = user.profile_img_file.id
    return output


def fileToDictionary(file) ->dict:
    output = {"id": file.id, "file_name": file.data.name.split("/")[-1], "file_type_id": file.file_type_id,
              "size": file.data.size, "created_at": file.created_at,
              "updated_at": file.updated_at}
    return output


def typeToDictionary(type) ->dict:
    output = {"id": type.id, "name": type.name};
    return output


def update_model(self, key, value):
    getattr(self, key)
    setattr(self, key, value)
