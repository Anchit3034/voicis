import ollama
import traceback

from memory.context_manager import (
    build_context,
    add_response
)

MODEL = "tinyllama"

def stream_llm(prompt):

    try:

        context = build_context(
            prompt
        )

        response_text = ""

        stream = ollama.chat(
            model=MODEL,
            messages=context,
            stream=True
        )

        for chunk in stream:

            try:

                token = (
                    chunk["message"]
                    ["content"]
                )

                response_text += token

                yield token

            except Exception:

                print(
                    "\n[OLLAMA TOKEN ERROR]"
                )

                traceback.print_exc()

        add_response(response_text)

    except Exception:

        print(
            "\n[OLLAMA ERROR]"
        )

        traceback.print_exc()
