from datetime import datetime
from typing import Set

from pydantic import AnyHttpUrl, BaseModel


class GivenElement(BaseModel):
    url: AnyHttpUrl
    name: str
    tags: Set[str] = set()

class SavedElement(GivenElement):
    id: str
    timestamp: datetime
