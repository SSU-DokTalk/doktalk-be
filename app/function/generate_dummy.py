from app.function.dummy_data import ko, en
from app.enums import LANGUAGE
from app.var import DEFAULT_LANGUAGE


def generate_sentence(
    original: str, language: LANGUAGE = LANGUAGE(DEFAULT_LANGUAGE)
) -> str:
    """
    original 문장을 이용해 dummy 문장 생성
    """
    results = []
    paragraphs = original.split("\n")
    dummy = read_dummy_sentence(language)

    for paragraph in paragraphs:
        idx = 0
        result = ""
        words = paragraph.split(" ")
        for word in words:
            result += dummy[idx % len(dummy) : (idx + len(word)) % len(dummy)] + " "
            idx += len(word)
        results.append(result)

    return "\n".join(results)


def read_dummy_sentence(language: LANGUAGE) -> str:
    """
    더미 문장을 반환
    """
    if language.value in ["us"]:
        return en.replace("\n", " ").replace(" ", "")
    return ko.replace("\n", " ").replace(" ", "")


__all__ = ["generate_sentence"]
