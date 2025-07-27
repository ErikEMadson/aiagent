import os
import dotenv
import sys

from google import genai
from google.genai import types

def main():
    dotenv.load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if len(sys.argv) < 2:
        print("Usage: uv run main.py <prompt string> [--verbose]")
        return

    user_prompt = sys.argv[1]

    verbose = False
    if len(sys.argv) >= 2:
        if sys.argv[2] == "--verbose":
            verbose = True
        else:
            print("Usage: uv run main.py <prompt string> [--verbose]")
            return


    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )

    print(response.text)

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
