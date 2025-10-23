import os
from config import MAX_CHARS

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory.lstrip("/"))

    if directory.startswith(".."):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
           
    
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
           
    
    contents_of_the_directory = ""
    for content in os.listdir(full_path):
        contents_of_the_directory += f"- {content}: file_size={os.path.getsize(os.path.join(full_path, content))} bytes, is_dir={os.path.isdir(os.path.join(full_path, content))}\n"
    return contents_of_the_directory
    

def get_file_content(working_directory, file_path):
    try:

        targer_path = os.path.abspath(os.path.join(working_directory, file_path)) #Si alguna de las rutas es absoluta, ignora working_directory.

        if not targer_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(targer_path):
            return f'Error: File not found or is not a regular file: {file_path}'
        
        with open(targer_path, 'r') as file:
            file_content_string = file.read(MAX_CHARS + 1)
            if len(file_content_string) > MAX_CHARS:
                return file_content_string[:MAX_CHARS] + f'\n[...File "{file_path}" truncated at 10000 characters]'
            else:
                return file_content_string
    except Exception as e:
        return f'Error: {str(e)}'
    
