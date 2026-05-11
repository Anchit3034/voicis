conversation_memory=[]

MAX_HISTORY=8

def build_context(prompt):
    global conversation_memory

    conversation_memory.apprnd({
        "role":"user",
        "content":prompt
        })
    converstion_memory=(conversation_memory[-MAX_HISTORY:])

    return conversation_memory
def add_response(response):
    conversation_memory.append({"role","assistant",
                                "content":response})

