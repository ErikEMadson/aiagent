import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a specified Python file located in the working directory. "
        "Runs the script and captures its output (stdout, stderr, and any non-zero returncode) so it can be reviewed or used in further steps."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The relative path (from the working directory) of the Python file to execute. "
                    "Must end with '.py'."
                ),
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description=(
                    "Optional list of command-line arguments to pass to the script during execution. "
                    "Each argument should be a string."
                ),
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):
    if args is None:
        args = []
    absolute_working_directory = os.path.abspath(working_directory) + os.sep
    full_path = os.path.abspath(os.path.join(absolute_working_directory, file_path))
    if not full_path.startswith(absolute_working_directory):
        return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
    if not os.path.exists(full_path):
        return f"Error: File \"{file_path}\" not found."
    if not full_path.endswith(".py"):
        f"Error: \"{file_path}\" is not a Python file."

    try:
        results = subprocess.run(["python3", full_path] + args, timeout=30, capture_output=True, cwd=absolute_working_directory)
        stdout = f"STDOUT:\n{results.stdout.decode()}\n\n" if len(results.stdout.decode()) > 0 else ""
        stderr = f"STDERR:\n{results.stderr.decode()}\n\n" if len(results.stderr.decode()) > 0 else ""
        returncode = f"Process exited with code {results.returncode}\n\n" if results.returncode != 0 else ""
        result_string = f"{stdout}{stderr}{returncode}"
        if len(result_string) == 0:
            result_string = "No output produced"
        return result_string
    except Exception as e:
        return f"Error: executing Python file: {e}"
