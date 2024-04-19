from mistralai.models.chat_completion import ChatMessage
import xml.etree.ElementTree as ET
import json
import re


class CodeAnalysisModel:
    """
    This class represents the Code Analysis model in the Zenith project.
    It is responsible for analyzing code to understand its language, structure,
    and purpose, and to generate relevant insights.
    """

    def __init__(self):
        """
        Initializes the Code Analysis Model.
        """
        pass

    def train(self, training_dataset):
        """
        Trains the Code Analysis model using the provided dataset.

        :param training_dataset: The dataset used for training the model.
        """
        pass

    def predict(self, prompt_file, code_file, output_file, client, model):
        """
        Predicts the output using the Code Analysis model based on the given input prompt
        and prediction dataset.

        :param input_prompt: The prompt used for making predictions.
        :param prediction_dataset: The dataset used for making predictions.
        :return: The prediction result.
        """
        self.code = ""
        try:
            with open(code_file, "r") as file:
                self.code = file.read()
        except FileNotFoundError:
            print("The code works")

        with open(prompt_file, "r") as file:
            prompt = file.read()

        full_prompt = prompt + self.code

        chat_response = client.chat(
            model=model,
            messages=[ChatMessage(role="user", content=full_prompt)],
        )
        # Open the file at the specified path in write ('w') mode
        self.output = chat_response.choices[0].message.content
        with open(output_file, "w") as file:
            # Write the data to the file
            file.write(chat_response.choices[0].message.content)

    def format_output_data(self):
        # Define patterns to match the HTML-like tags
        xml_data = self.output
        root = ET.fromstring(xml_data)

        # Extract data and construct the dictionary
        analysis_dict = {
            "code": self.code,  # Assuming 'code' needs to be filled with actual source code or another value
            "language_label": root.find("language").text,
            "overall_description": root.find("description").text,
            "components": [
                {
                    "type": comp.find("type").text,
                    "name": comp.find("name").text,
                    "description": comp.find("desc").text,
                }
                for comp in root.find("components")
            ],
        }

        # Serialize dictionary to JSON
        json_data = json.dumps(analysis_dict, indent=4)

        return json_data
