import re
URL_PTN = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"

def has_url(text: str):
    result = re.match(URL_PTN, text)

    if result:
        return True
    return False    