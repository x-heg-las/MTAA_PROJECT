ticket_schema = {
    "type": "object",
    "$schema": "http://json-schema.org/draft-07/schema",
    "id": "http://jsonschema.net",
    "properties": {
        "title": {
            "type": "string",
        },
        "user_id": {
            "type": "number"
        },
        "descrption": {
            "type": "string"
        },
        "request_type_id": {
            "type": "number"
        },
        "call_requested": {
            "type": "boolean"
        }
    },
    "required": ["title", "user_id", "description", "request_type_id", "call_requested"]
}

ticket_schema_update = {
    "type": "object",
    "$schema": "http://json-schema.org/draft-07/schema",
    "id": "http://jsonschema.net",
    "properties": {
        "title": {
            "type": "string",
        },
        "user_id": {
            "type": "number"
        },
        "descrption": {
            "type": "string"
        },
        "request_type_id": {
            "type": "number"
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
        "user_type_id": {
            "type": "number"
        },
        "profile_img_file_id": {
            "type": "number"
        }
    },
    "required": ["username", "full_name", "phone_number", "profile_img_file_id", "user_type_id"]
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
        "user_type_id": {
            "type": "number"
        },
        "profile_img_file_id": {
            "type": "number"
        }
    },
}