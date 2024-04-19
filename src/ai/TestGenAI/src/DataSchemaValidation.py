import json
import jsonschema
from jsonschema import validate
from jsonschema.exceptions import ValidationError


def load_schema(schema_path):
    """
    Loads the JSON schema from a file.

    :param schema_path: Path to the JSON schema file.
    :return: The loaded schema.
    """
    with open(schema_path, "r") as file:
        return json.load(file)


def validate_json(json_data, schema):
    """
    Validates a JSON dataset against the provided schema.

    :param json_data: The JSON data to be validated.
    :param schema: The JSON schema against which to validate.
    :return: None. Raises an exception if validation fails.
    """
    try:
        validate(instance=json_data, schema=schema)
        print("JSON data is valid.")
    except ValidationError as e:
        print(f"JSON validation error: {e.message}")
        raise


def single_json(schema_file, json_file):
    # Example Usage

    schema = load_schema(schema_file)
    with open(json_file, "r") as file:
        data = json.load(file)
        validate_json(data, schema)


def multiple_json(schema_files, json_files):
    # Example Usage

    for schema_file, json_file in zip(schema_files, json_files):
        schema = load_schema(schema_file)
        with open(json_file, "r") as file:
            data = json.load(file)
            print(f"Validating {json_file} against {schema_file}...")
            validate_json(data, schema)


#! Single file use
# schema_file = "data/validation/CodeAnalysisSchema.json"
# json_file = "data/CodeAnalysis.json"

schema_files = [
    "data/validation/CodeAnalysisSchema.json",
    "data/validation/TestGenerationSchema.json",
    "data/validation/CodeAnalysisSchema.json",
]
json_files = [
    "data/CodeAnalysis.json",
    "data/CodeAnalysis.json",
    "data/TestGeneration.json",
]


multiple_json(schema_files, json_files)
