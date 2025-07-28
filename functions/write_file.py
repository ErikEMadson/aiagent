import os

def write_file(working_directory, file_path, content):
    absolute_working_directory = os.path.abspath(working_directory) + os.sep
    full_path = os.path.abspath(os.path.join(absolute_working_directory, file_path))
    if not full_path.startswith(absolute_working_directory):
        return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
    if not os.path.exists(os.path.dirname(full_path)):
        try:
            os.makedirs(os.path.dirname(full_path))
        except:
            return f"Error: could not create the containing directories for \"{file_path}\""
    if os.path.isdir(full_path):
        return f"Error: File not found or is not a regular file: \"{file_path}\""

    try:
        with open(full_path, "w") as file:
            file.write(content)
        return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
    except Exception:
        return "Error: An error occured while writing to \"{file_path}\""
