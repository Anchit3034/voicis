import ollama

from memory.context_manager import(
        build_context,
        add_response
        )
MODEL="mistral"

def ask_llm(prompt):
    context=build_context(prompt)
    response=ollama.chat(model=MODOL,messages=context)
    text=response["message"]["content"]


    add_response(text)

    return text

