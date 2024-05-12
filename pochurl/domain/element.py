from datetime import datetime
from typing import Set

from pydantic import AnyHttpUrl, BaseModel


class GivenElement(BaseModel):
    url: AnyHttpUrl
    name: str
    tags: Set[str] = set()

    class Config:
        json_schema_extra = {
            "examples": [
                {"url": "https://example1.py", "name": "name1", "tags": ["tag1", "tag2"]},
            ]
        }


class SavedElement(GivenElement):
    id: str
    timestamp: datetime
