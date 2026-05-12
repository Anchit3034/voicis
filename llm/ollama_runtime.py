import ollama

from memory.context_manager import (
    build_context,
    add_response
)

MODEL = "mistral"

def stream_llm(prompt):

    context = build_context(prompt)

    stream = ollama.chat(
        model=MODEL,
        messages=context,
        stream=True
    )

    response_text = ""

    for chunk in stream:

        token = chunk[
            "message"
        ]["content"]

        response_text += token

        yield token

    add_response(response_text)
