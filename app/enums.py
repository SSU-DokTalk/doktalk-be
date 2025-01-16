from enum import Enum, IntEnum


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


class CATEGORY(IntEnum):
    POLITICS = 1 << 0
    HUMANITIES = 1 << 1
    ECONOMY = 1 << 2
    HISTORY = 1 << 3
    SCIENCE = 1 << 4
    ESSAY = 1 << 5
    TEENAGER = 1 << 6
    CHILD = 1 << 7

    @classmethod
    def from_num(cls, cat_num: int):
        cat_list = list()
        for enum in cls:
            if enum.value & cat_num == cat_num:
                cat_list.append(enum)
        return cat_list

    @classmethod
    def max(cls):
        return 2 ** len(cls) - 1


__all__ = ["PROVIDER", "ROLE", "LANGUAGE", "CATEGORY"]
