from . import schemas
from jsonschema import validate, exceptions, ErrorTree, Draft7Validator

tickets_fields = ["title", "user", "description", "request_type__name", "call_requested", "file", "answered_by_user"]
users_fields = ["username", "full_name", "phone_number", "profile_img_file", "user_type__name", "password"]


def validateTicketEntry(data, updating=False):
    result = {"success": True, "errors": {}}
    errors = []
    try:
        for key in data:
            if not key in tickets_fields:
                result["success"] = False
                errors.append(
                    {
                        "field": key,
                        "reason": "non-existing parameter"
                    }
                )
        if updating:
            if len(data) == 0:
                result["success"] = False
                errors.append(
                    {
                        "field": "any",
                        "reason": "at least one parameter must be specified"
                    }
                )
            validate(data, schemas.ticket_schema_update)
        else:
            validate(data, schemas.ticket_schema)
    except exceptions.ValidationError:
        result["success"] = False
        validator = Draft7Validator(schemas.ticket_schema)
        error_tree = ErrorTree(validator.iter_errors(data))

        for key in tickets_fields:
            if key in error_tree:
                errors.append(
                    {
                        "field": key,
                        "reason": "wrong value"
                    }
                )
                continue

            if not key in data and not updating:
                errors.append(
                    {
                        "field": key,
                        "reason": "missing"
                    }
                )

    finally:
        result["errors"] = errors
        return result


def validateUserEntry(data, updating=False):
    result = {"success": True, "errors": {}}
    errors = []
    try:
        for key in data:
            if not key in users_fields:
                result["success"] = False
                errors.append({
                    "field": key,
                    "reason": "non-existing parameter"
                }
                )
        if updating:
            if len(data) == 0:
                result["success"] = False
                errors.append(
                    {
                        "field": "any",
                        "reason": "at least one parameter must be specified"
                    }
                )
            validate(data, schemas.user_schema_update)
        else:
            validate(data, schemas.user_schema)
    except exceptions.ValidationError:
        result["success"] = False
        validator = Draft7Validator(schemas.user_schema)
        error_tree = ErrorTree(validator.iter_errors(data))

        for key in users_fields:
            if not key in data and not updating:
                errors.append(
                    {
                        "field": key,
                        "reason": "missing"
                    }
                )

            if key in error_tree:
                errors.append(
                    {
                        "field": key,
                        "reason": "wrong value"
                    }
                )

    finally:
        result["errors"] = errors
        return result
