from datetime import datetime
from typing import Set

from pydantic import AnyHttpUrl, BaseModel


class GivenElement(BaseModel):
    url: AnyHttpUrl
    name: str
    tags: Set[str]

class SavedElement(GivenElement):
    timestamp: datetime
