import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file


def main():
    print(os.sys.argv)

    system_prompt = system_prompt = """
                                    Sos un asistente de programacion experto en Python.
                                    Tu tarea es ayudar al usuario a realizar tareas de programacion en un proyecto de Python.
                                    Para ello, puedes utilizar las siguientes funciones, haciendo un plan y llamandolas de manera iterativa y conjunta:
                                    - get_files_info: Obtiene informacion sobre los archivos en el directorio de trabajo.
                                    - get_file_content: Obtiene el contenido de un archivo especifico.
                                    - write_file: Escribe contenido en un archivo especifico.
                                    - run_python_file: Ejecuta un archivo Python y devuelve su salida.
                                    Utiliza estas funciones de manera iterativa y conjunta para cumplir con la solicitud del usuario.
                                    Ejemplo: Si neceisttas ver el contnido de un archivo, primero usa get_files_info para encontrar el archivo,
                                    luego usa get_file_content para obtener su contenido, si necesitas modificarlo, usa write_file, y finalmente si necesitas ver el resultado de la modificacion, usa run_python_file.
                                    Siempre la primer funcion candidata debe ser get_files_info para obtener el contexto del proyecto, si no se pasa se un directorio es el directorio root.
                                    """
    working_directory = "./calculator"

    if not os.sys.argv:
        print("Error: No arguments provided")
        os.sys.exit(1)
    else:
        verbose = False
        if "--verbose" in os.sys.argv:
            verbose = True

        print("Hello from agent!")
        load_dotenv()

        api_key = os.environ.get("GEMINI_API_KEY")
        print(f"API Key: {api_key}")
        client = genai.Client(api_key=api_key)

        command_line_arg = os.sys.argv[1]

        messages = [
            types.Content(role="user", parts=[types.Part(text=command_line_arg)]),
        ]#Va a cotener la lista de mensajes para que la IA tenga contexto, cada mensaje tiene un rol y partes. Esta lista se pasa  generte_content.


        available_functions = types.Tool(
            function_declarations=[
                schema_get_files_info,schema_get_file_content,schema_write_file,schema_run_python_file
            ]
        )
        #print(f"-----------------{schema_run_python_file}----------------------")

        for i in range(20):
            try:
                response = generate_content(client, messages, system_prompt,available_functions)
                for candidate in response.candidates:
                    #print("--------------------------------------------------")
                    #print(candidate.content)
                    #print("--------------------------------------------------")
                    messages.append(candidate.content)

                
                #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                #print(f"Function calls in response: {response.candidates[0].content.parts[-1].function_call}")
                #print(response.function_calls)
                #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")


                if response.text and not response.function_calls:# Si la respuesta tiene texto, es que ya no hay mas llamadas a funciones que hacer.
                    print(f"Response text ----------> {response.candidates[0].content.parts[-1].text}")
                    break
                

                if response.function_calls:
                    for function_call_part in response.function_calls:
                        function_response = call_function(function_call_part,working_directory,verbose).parts[0].function_response.response
                        if not function_response:
                            raise ValueError("Function response is None")
                        if verbose:
                            print(f"-> {function_response["result"]}")
                        messages.append(types.Content(role="user", parts=[types.Part(text=function_response["result"])]))
                        #print("###########################")
                        #print(types.Content(role="user", parts=[types.Part(text=function_response["result"])]))
                        #print("###########################")
                #for i in messages: Debbug, para ver como cada lllamada a funcion la tranformo en un mensaje con rol de usuario.y queda intercalado con los mensaje s de modelos que hacen la llamadas a funciones.
                # print(f"{i.role}----{i}")

            except Exception as e:
                print(f"Error during content generation or function call: {e}")       

        if verbose:
            print(f"User prompt: {command_line_arg}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        


        #os.sys.exit(0)
                



def generate_content(client, messages, system_prompt,available_functions):

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt,tools=[available_functions])
    )
    return response



def call_function(function_call_part,working_directory, verbose=False ):
    if verbose:
        print(f"Calling : {function_call_part.name} with args: {function_call_part.args}")
    else:
        print(f"Calling function: {function_call_part.name}()")

    function_name = function_call_part.name
    match function_name:
        case "get_files_info":
            from functions.get_files_info import get_files_info
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": get_files_info(working_directory, **function_call_part.args)},
                    )
                ],
            )
        case "get_file_content":
            from functions.get_file_content import get_file_content
            return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": get_file_content(working_directory, **function_call_part.args)},
                )
            ],
        )
        case "write_file":
            from functions.write_file import write_file
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": write_file(working_directory, **function_call_part.args)},
                    )
                ],
            )
        case "run_python_file":
            from functions.run_python_file import run_python_file
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": run_python_file(working_directory,**function_call_part.args)},
                    )
                ],
            )
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )




if __name__ == "__main__":
    main()