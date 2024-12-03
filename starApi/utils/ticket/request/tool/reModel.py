import re
import unicodedata


def re_find_all(pattern, text):
    match = re.findall(pattern, text)
    if match:
        return match[0]
    else:
        return ""


def repl(str):
    result = re.sub(
        r"(\\u[a-zA-Z0-9]{4})",
        lambda x: x.group(1).encode("utf-8").decode("unicode-escape"),
        str,
    )
    result = re.sub(
        r"(\\r|\\n|\\t|\xa0|\\u[0-9]{4})", lambda x: "", result)
    result = unicodedata.normalize("NFKC", result)
    return result.strip()
