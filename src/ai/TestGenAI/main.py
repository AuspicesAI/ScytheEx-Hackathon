import os
from dotenv_vault import load_dotenv
import boto3
from mistralai.client import MistralClient
from zenith_models import CodeAnalysisModel, TestGenerationModel, CodeSuggestionModel
import json

load_dotenv(".env")


def fetch_code_file():

    s3_client = boto3.client("s3")

    bucket_name = "your-bucket-name"
    s3_prefix = "your/s3/prefix/"  # The S3 directory path where the file is located

    # List the files in the specified bucket and prefix
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=s3_prefix)

    # Assuming there is only one file in that directory or you have a way to identify it
    if "Contents" in response:
        file_info = response["Contents"][0]
        s3_file_key = file_info["Key"]
        file_name = s3_file_key.split("/")[-1]  # Extract the file name

        local_directory = "/data/code"  # Directory where you want to save the file
        local_file_path = os.path.join(local_directory, file_name)

        # Download the file
        s3_client.download_file(bucket_name, s3_file_key, local_file_path)

        print(f"File '{file_name}' downloaded to '{local_file_path}'")
    else:
        print("No files found in the specified S3 bucket and prefix.")

    return file_name


def save_user_data(code_analyzer_data):
    code_analyzer_json = "data/CodeAnalysis.json"

    # Ensure code_analyzer_data is in the correct format (as a dictionary)
    if isinstance(code_analyzer_data, str):
        # If it's a string, parse it into a dictionary
        code_analyzer_data = json.loads(code_analyzer_data)

    # Check if the file exists and then read its content; if not, initialize an empty list
    if os.path.exists(code_analyzer_json):
        with open(code_analyzer_json, "r") as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    # Append the new data to the existing data
    existing_data.append(code_analyzer_data)

    # Write the updated data back to the JSON file
    with open(code_analyzer_json, "w") as file:
        json.dump(existing_data, file, indent=4)


def main():

    code_analyzer = CodeAnalysisModel()
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-small"
    client = MistralClient(api_key=api_key)
    user_consent = False

    # code_filename = fetch_code_file()
    code_filename = "somefile.py"

    code_analyzer_prompt_filename = r"inputs/prompts/CodeAnalysis.txt"
    code_analyzer_filename = os.path.join(r"data/code/", code_filename)
    print(code_analyzer_filename)
    code_analyzer_output_filename = r"outputs/CodeAnalysis_result.xml"

    code_analyzer.predict(
        code_analyzer_prompt_filename,
        code_analyzer_filename,
        code_analyzer_output_filename,
        client,
        model,
    )
    code_analyzer_data = code_analyzer.format_output_data()

    user_consent = True
    if user_consent:
        save_user_data(code_analyzer_data)


if __name__ == "__main__":
    main()
