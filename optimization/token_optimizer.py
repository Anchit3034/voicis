import tiktoken
encoding = tiktoken.get_encoding("cl100k_base")

STOPWORDS={
        "please",
        "can you",
        "could you",
        "um",
        "uh",
        "actually",
        "basically"
        }
def optimize_prompt(text):
    text=text.lower()
    for word in STOPWORDS:
        text=text.replace(word,"")
    
    text=" ".join(text.split())
    return text
def token_count(text):
    return len(encodeing.encode(text))

