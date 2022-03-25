def requestToDictionary(request) ->dict:
    output = {"id": request.id, "title": request.title, "user_id": request.user.id,
              "request_type_id": request.request_type.id, "description": request.description,
              "call_reqested": request.call_requested, "created_at": request.created_at,
              "updated_at": request.updated_at}
    return output


def userToDictionaru(user) ->dict:
    output = {"id": user.id, "username": user.username, "user_type_id": user.user_type.id,
              "full_name": user.full_name, "phone_number": user.phone_number, "created_at": user.created_at,
              "updated_at": user.updated_at}
    if user.profile_img_file:
        output["profile_img_file_id"] = user.profile_img_file.id
    return output


def fileToDictionary(file) ->dict:
    output = {"id": file.id, "file_name": file.data.name.split("/")[-1], "file_type_id": file.file_type_id,
              "size": file.data.size, "created_at": file.created_at,
              "updated_at": file.updated_at}
    return output


def update_model(self, key, value):
    getattr(self, key)
    setattr(self, key, value)
