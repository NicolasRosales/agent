import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file.",
            ),
        },
    ),
)



def write_file(working_directory, file_path, content):
    try:
        base_dir = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(base_dir, file_path))

        if not target_path.startswith(base_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        

        with open(target_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error writing file: {e}"