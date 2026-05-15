

DEBUG = False

def debug(message):

    if DEBUG:

        print(
            f"[DEBUG] {message}"
        )

def info(message):

    print(
        f"[INFO] {message}"
    )

def error(message):

    print(
        f"[ERROR] {message}"
    )
