import  os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_target_path = os.path.abspath(os.path.join(working_directory, file_path))
        abs_working_directory = os.path.abspath(working_directory)   
        if not abs_target_path.startswith(abs_working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_target_path):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith('.py'):
            return f'Error: File "{file_path}" is not a Python file.'
        
        list= ["python3", abs_target_path] + args
        
        completed_process = subprocess.run(list,timeout=30,capture_output=True,cwd=abs_working_directory,text=True)
        if completed_process.returncode == 0:
            return f"STDOUT: {completed_process.stdout}"
        else:
            return f"STDERR: {completed_process.stderr} - Process exited with code {completed_process.returncode}"

        # Terminanr de escribir la función para ejecutar el archivo Python
    except Exception as e:
        return f"Error: executing Python file: {e}"   

    
