import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    if(len(sys.argv)<2):
        print("Error")
        sys.exit(1)
    else:
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        
        user_prompt = sys.argv[1]
        messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

        print("Hello from agent!")

        response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages)
        print(response.text)
        if len(sys.argv)==3 and sys.argv[2] and sys.argv[2] == "--verbose":
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
