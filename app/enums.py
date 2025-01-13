from enum import Enum


class PROVIDER(Enum):
    KAKAO = "kakao"
    NAVER = "naver"
    GOOGLE = "google"
    FACEBOOK = "facebook"

    @classmethod
    def from_str(cls, name: str):
        for enum in cls:
            if enum.value == name:
                return enum


class ROLE(Enum):
    ADMIN = "ADMIN"
    USER = "USER"

    @classmethod
    def from_str(cls, name: str):
        for enum in cls:
            if enum.value == name:
                return enum


class LANGUAGE(Enum):
    KR = "kr"
    US = "us"

    @classmethod
    def from_str(cls, name: str):
        for enum in cls:
            if enum.value == name:
                return enum
        return cls.KR


__all__ = ["PROVIDER", "ROLE", "LANGUAGE"]
