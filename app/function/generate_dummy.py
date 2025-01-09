from typing import Literal
from app.function.dummy_data import ko, en


def generate_sentence(original: str, language: Literal["ko", "en"] = "ko") -> str:
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


def read_dummy_sentence(language: Literal["ko", "en"]) -> str:
    """
    더미 문장을 반환
    """
    if not language in ["ko", "en"]:
        raise ValueError("지원하지 않는 언어입니다.")
    if language == "ko":
        return ko.replace("\n", " ").replace(" ", "")
    elif language == "en":
        return en.replace("\n", " ").replace(" ", "")


__all__ = ["generate_sentence"]
