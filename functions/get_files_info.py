import os

def get_files_info(working_directory, directory="."):
    absolute_working_directory = os.path.abspath(working_directory) + os.sep
    full_path = os.path.abspath(os.path.join(absolute_working_directory, directory)) + os.sep
    if not full_path.startswith(absolute_working_directory):
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
    if not os.path.isdir(full_path):
        return f"Error: \"{directory}\" is not a directory"

    try:
        file_list = os.listdir(full_path)
    except Exception:
        return f"Error: unable to get the listing for the directory \"{directory}\""

    if absolute_working_directory == full_path:
        return_string = "Result for current directory:\n"
    else:
        return_string = f"Result for '{directory}' directory:\n"

    for file_name in file_list:
        return_string = f"{return_string}- {file_name}: file_size="
        try:
            file_size=os.path.getsize(os.path.join(full_path, file_name))
            return_string = f"{return_string}{file_size} bytes, is_dir="
        except Exception:
            return f"Error: Unable to get the size of \"{file_name}\" in \"{directory}\""

        try:
            is_directory = not os.path.isfile(os.path.join(full_path, file_name))
            return_string = f"{return_string}{is_directory}\n"
        except Exception:
            return f"Error: Unable to determine if \"{file_name}\" in \"{directory}\" is a directory"

    return return_string
