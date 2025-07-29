import os
import config

from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        "Retrieves the full content of a specified file, constrained to the working directory. "
        "Useful for reading the contents of text files like, for example, code or configuration files so they can be analyzed or modified."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The relative path (from the working directory) of the file to read. "
                    "Must point to a valid file within the working directory."
                ),
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    absolute_working_directory = os.path.abspath(working_directory) + os.sep
    full_path = os.path.abspath(os.path.join(absolute_working_directory, file_path))
    if not full_path.startswith(absolute_working_directory):
        return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
    if os.path.isdir(full_path):
        return f"Error: File not found or is not a regular file: \"{file_path}\""

    try:
        with open(full_path, "r") as file:
            file_content_string = file.read(config.MAX_CHARS + 1)
    except Exception:
        return "Error: Unable to read the contents of \"{file_path}\""

    if len(file_content_string) > config.MAX_CHARS:
        file_content_string = f"{file_content_string[:config.MAX_CHARS]}\n\n[...File \"{file_path}\" truncated at 10000 characters]"

    return file_content_string
