import os


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