from typing import List

from pydantic import BaseModel


class AddResponse(BaseModel):
    added_ids: List[str]
    errors: List[dict] = []
