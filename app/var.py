from typing import Literal

# book title, item title
SEARCHBY = Literal["bt", "it"]
DEFAULT_SEARCHBY = "bt"

# latest, popular
SORTBY = Literal["latest", "popular"]
EXT_SORTBY = Literal["latest", "popular", "from"]
DEFAULT_SORTBY = "latest"

# korean, english
DEFAULT_LANGUAGE = "kr"

__all__ = [
    "SEARCHBY",
    "DEFAULT_SEARCHBY",
    "SORTBY",
    "EXT_SORTBY",
    "DEFAULT_SORTBY",
    "DEFAULT_LANGUAGE",
]
