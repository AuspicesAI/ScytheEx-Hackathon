import os
from dotenv_vault import load_dotenv
import boto3
from mistralai.client import MistralClient
from zenith_models import CodeAnalysisModel, TestGenerationModel, CodeSuggestionModel

load_dotenv(".env")
api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-small"
client = MistralClient(api_key=api_key)
user_consent = False
s3 = boto3.client("s3")
bucket_name = "zenith-testgenai-s3"
code_analyzer = CodeAnalysisModel()


def fetch_code_file_from_s3():
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix="code-queue")

    if "Contents" in response:
        for file_info in response["Contents"]:
            if not file_info["Key"].endswith("/") and file_info["Size"] > 0:
                s3_file_key = file_info["Key"]
                file_name = file_info["Key"].split("/")[-1]

        local_directory = "data/code"  # Directory where you want to save the file
        if not os.path.exists(local_directory):
            os.makedirs(local_directory)  # Create the directory if it doesn't exist

        local_file_path = os.path.join(local_directory, file_name)
        print(file_name)
        # Download the file
        s3.download_file(bucket_name, s3_file_key, local_file_path)

        print(f"File '{file_name}' downloaded to '{local_file_path}'")
    else:
        print("No files found in the specified S3 bucket and prefix.")
        file_name = None

    return file_name


def upload_output_file_to_s3(file_name):

    local_file_path = "outputs" + file_name
    s3_path = "generated-tests" + file_name
    s3.upload_file(local_file_path, bucket_name, s3_path)


def save_user_data(code_analyzer_data):
    code_analyzer.save_user_data(code_analyzer_data)


def analyze_code(code_filename):

    # code_filename = fetch_code_file()

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

    return code_analyzer.format_output_data()


def main():

    code_filename = fetch_code_file_from_s3()
    # test_filename = "/test_" + code_filename

    # upload_output_file_to_s3(test_filename)

    code_analyzer_data = analyze_code(code_filename)

    # if user_consent:
    #     save_user_data(code_analyzer_data)


if __name__ == "__main__":
    main()
