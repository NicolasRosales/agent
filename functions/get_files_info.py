import os
from config import MAX_CHARS
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    try:
        base_dir = os.path.abspath(working_directory)
        target_dir = os.path.abspath(os.path.join(base_dir, directory))# En el join si una ruta es absoluta, ignora las anteriores y toma esa como base.

        #print(f"Base directory: {base_dir}")
        #print(f"Target directory: {target_dir}")

        if not target_dir.startswith(base_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        dir_info = ""
        for path_in_target in os.listdir(target_dir):
            full_path = os.path.join(target_dir, path_in_target)
            dir_info += f"- {path_in_target}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}\n"

        return dir_info
    except Exception as e:
        return f"Error: {str(e)}"


    