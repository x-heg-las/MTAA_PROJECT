ticket_schema = {
    "type": "object",
    "$schema": "http://json-schema.org/draft-07/schema",
    "id": "http://jsonschema.net",
    "properties": {
        "title": {
            "type": "string",
        },
        "user": {
            "type": "number"
        },
        "descrption": {
            "type": "string"
        },
        "request_type__name": {
            "type": "string"
        },
        "call_requested": {
            "type": "boolean"
        }
    },
    "required": ["title", "user", "description", "request_type__name", "call_requested"]
}

ticket_schema_update = {
    "type": "object",
    "$schema": "http://json-schema.org/draft-07/schema",
    "id": "http://jsonschema.net",
    "properties": {
        "title": {
            "type": "string",
        },
        "user": {
            "type": "number"
        },
        "descrption": {
            "type": "string"
        },
        "request_type__name": {
            "type": "string"
        },
        "call_requested": {
            "type": "boolean"
        }
    },
}

user_schema = {
    "type": "object",
    "$schema": "http://json-schema.org/draft-07/schema",
    "id": "http://jsonschema.net",
    "properties": {
        "username": {
            "type": "string"
        },
        "password": {
            "type": "string"
        },
        "phone_number": {
            "type": "string"
        },
        "full_name": {
            "type": "string"
        },
        "user_type__name": {
            "type": "string"
        },
        "profile_img_file": {
            "type": ["number", "null"]
        }
    },
    "required": ["username", "full_name", "phone_number", "profile_img_file", "user_type__name"]
}

user_schema_update = {
    "type": "object",
    "$schema": "http://json-schema.org/draft-07/schema",
    "id": "http://jsonschema.net",
    "properties": {
        "username": {
            "type": "string"
        },
        "password": {
            "type": "string"
        },
        "phone_number": {
            "type": "string"
        },
        "full_name": {
            "type": "string"
        },
        "user_type__name": {
            "type": "string"
        },
        "profile_img_file": {
            "type": ["number", "null"]
        }
    },
}