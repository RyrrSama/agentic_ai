import os
from typing import Dict, List

import litellm
from litellm import completion

os.environ["LM_STUDIO_API_KEY"] = "http://localhost:1234/v1"


def extract_python_codeblock(response):
    response = response.replace("```", "")
    if response.startswith("python"):
        response = response[6:]
    return response


def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response"""

    response = completion(
        model=os.environ["MODEL"],
        messages=messages,
        max_tokens=1024,
        timeout=1000,
        base_url=os.environ["API_BASE_URL"],
        api_key="",
        stream=True,
    )
    full_response = ""
    for chunk in response:
        content = chunk["choices"][0]["delta"]["content"]
        print(content, end="", flush=True)  # Print without newline and flush output
        full_response += content or ""
    print()  # Add a newline after the response is fully generated

    return full_response


response = ""
message = []
message.append(
    {
        "role": "system",
        "content": "You are expert python software developer. You should support the user to write python code function for given function description. Your response should contain python code blocks only.",
    }
)

while 1:
    input_str = input("User: ")
    if input_str.lower() == "exit":
        break

    message.append({"role": "assistant", "content": response})
    message.append({"role": "user", "content": input_str})
    response = generate_response(message)
    print("Agentic-AI : ", extract_python_codeblock(response), "\n")
