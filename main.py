import os
import dotenv
import sys

import config
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

from google import genai
from google.genai import types

# def call_function(function_call_part, verbose=False):



def main():
    dotenv.load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if len(sys.argv) < 2:
        print("Usage: uv run main.py <prompt string> [--verbose]")
        return

    user_prompt = sys.argv[1]

    verbose = False
    if len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":
            verbose = True
        else:
            print("Usage: uv run main.py <prompt string> [--verbose]")
            return


    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=config.SYSTEM_PROMPT
        )
    )

    for part in response.candidates[0].content.parts:
        if part.text:
            print(part.text)
        if part.function_call:
            print(f"Calling function: {part.function_call.name}({part.function_call.args})")

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
