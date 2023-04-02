import json

with open("schema_introspection.json", "r") as f:
    introspection_data = json.load(f)


def generate_query(type_name: str, introspection_data: dict) -> str:
    query_fields = []
    types = introspection_data["__schema"]["types"]

    def get_nested_fields(field_type: dict) -> str:
        if "fields" in field_type:
            nested_fields = []
            for nested_field in field_type["fields"]:
                field_name = nested_field["name"]
                field_type_name = nested_field["type"]["name"] or nested_field["type"]["ofType"]["name"]
                nested_fields.append(f"{field_name}: {field_type_name}")
            return "{" + ", ".join(nested_fields) + "}"
        return ""

    for type_data in types:
        if type_data["name"] == type_name:
            for field in type_data["fields"]:
                if not field["isDeprecated"]:
                    field_name = field["name"]
                    field_description = field["description"]

                    # Generate arguments schema
                    field_args = []
                    for arg in field["args"]:
                        arg_name = arg["name"]
                        arg_type = arg["type"]["name"] or arg["type"]["ofType"]["name"]
                        field_args.append(f"{arg_name}: {arg_type}")

                    field_args_str = f"({', '.join(field_args)})" if field_args else ""

                    # Get nested fields schema
                    field_return_type = field["type"]
                    while "ofType" in field_return_type and field_return_type["ofType"]:
                        field_return_type = field_return_type["ofType"]

                    nested_fields = get_nested_fields(field_return_type)

                    query_fields.append(f"# {field_description}\n{field_name}{field_args_str} {nested_fields}")

            break

    if not query_fields:
        return None

    return f"{{\n  {type_name} {{\n    " + "\n    ".join(query_fields) + "\n  }}\n}}"

type_name = "Query"
query_string = generate_query(type_name, introspection_data)
print(query_string)

