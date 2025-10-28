import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run o execute a specified Python file within the working directory and returns its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="A list of command-line arguments to pass to the Python file. It is optional.",
                
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    try:
        base_dir = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(base_dir, file_path))

        if not target_path.startswith(base_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(target_path):
            return f'Error: File "{file_path}" not found.'
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        commmand = ["python3", target_path] + args
        completed_process = subprocess.run(commmand,
                                           timeout=30,
                                           cwd=base_dir,
                                           text=True,
                                           capture_output=True)   

        output = ""  
        if completed_process.stdout:
            output += f"STDOUT:\n{completed_process.stdout}\n"
        if completed_process.stderr:
            output += f"STDERR:\n{completed_process.stderr}\n"
        if output:
            output += f"Process exited with code {completed_process.returncode}\n"
            return output
        return  "No output produced."
  

    except Exception as e:
        return f"Error: executing Python file: {e}"