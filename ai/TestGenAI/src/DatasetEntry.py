import gradio as gr
import json
import os


def update_json_file(code_filename, json_filename, file_key):
    base_dir = os.path.dirname(
        os.path.dirname(__file__)
    )  # This navigates two levels up from the current script

    # Construct the file path and read the code file
    code_file_path = os.path.join(base_dir, "data/code", code_filename)
    with open(code_file_path, "r") as file:
        code_content = file.read()

    # Construct the path to the JSON file
    json_file_path = os.path.join(base_dir, "data", f"{json_filename}.json")

    # Read the existing JSON file
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)
    else:
        data = {}

        # Update the specific entry in the JSON data
    updated = False
    for entry in data:
        if entry.get("file") == file_key:
            entry["code"] = code_content
            updated = True
            break

    if not updated:
        return f"No entry found with file key: {file_key}"

    # Write the updated data back to the JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

    return "JSON file updated successfully."


def main():
    with gr.Blocks() as demo:
        gr.Markdown("### Update JSON File with Code Content")

        with gr.Row():
            code_filename = gr.Textbox(label="Code Filename")
            json_filename = gr.Textbox(label="JSON Filename")
            file_key = gr.Textbox(label="File Key in JSON")

        submit = gr.Button("Update JSON File")
        output = gr.Markdown()

        submit.click(
            fn=update_json_file,
            inputs=[code_filename, json_filename, file_key],
            outputs=output,
        )

    demo.launch()


if __name__ == "__main__":
    main()
