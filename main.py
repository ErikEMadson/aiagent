import os
import dotenv
import sys
import time

import config
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

from google import genai
from google.genai import types

function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file
}

def call_function(function_call_part, verbose=False, working_directory="."):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    try:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": function_map[function_call_part.name](working_directory, **function_call_part.args)},
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"{e}"}
                )
            ],
        )

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

    awaiting_response = True
    while awaiting_response:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=config.SYSTEM_PROMPT
                )
            )
            awaiting_response = False
        except Exception:
            time.sleep(5)


    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    i = 0

    while True:
        i += 1
        if verbose:
            print(f"---Iteration {i}---")

        done = True
        for candidate in response.candidates:
            messages.append(candidate.content)
            for part in candidate.content.parts:
                if part.text:
                    print(part.text)
                if part.function_call:
                    result = call_function(part.function_call, verbose, config.WORKING_DIRECTORY)
                    if not result.parts[0].function_response.response:
                        raise Exception("There was no function response")
                    if verbose:
                        print(f"-> {result.parts[0].function_response.response}")
                    messages.append(result)
                    done = False
        if done or i >= config.MAX_ITERATIONS:
            break

        awaiting_response = True
        while awaiting_response:
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash-001",
                    contents=messages,
                    config=types.GenerateContentConfig(
                        tools=[available_functions],
                        system_instruction=config.SYSTEM_PROMPT
                    )
                )
                awaiting_response = False
            except Exception:
                time.sleep(5)


if __name__ == "__main__":
    main()
