import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write or overwrite a specified file with given content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write to, relative to the working directory.",
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

        targer_path = os.path.abspath(os.path.join(working_directory, file_path)) #Si alguna de las rutas es absoluta, ignora working_directory.

        if not targer_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
        with open(targer_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        

    except Exception as e:
        return f'Error: {str(e)}'