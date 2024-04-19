# base_model.py
import jsonschema
from jsonschema import validate


class BaseModel:
    """
    A base class for the models in the Zenith project, providing common functionalities
    like dataset validation.
    """

    def validate_dataset(self, dataset, schema):
        """
        Validates a given JSON dataset against a custom schema.
        :param dataset: The JSON dataset to be validated.
        :param schema: The JSON schema that defines the structure and types of the dataset.
        :return: Boolean indicating whether the dataset is valid or not.
        :raises jsonschema.exceptions.ValidationError: If the dataset does not conform to the schema.
        """
        try:
            validate(instance=dataset, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            print(f"Dataset validation error: {e}")
            return False
