from typing import Literal, Set

from pydantic import AnyHttpUrl, BaseModel


TagList = Literal["👀", "✨", "🚨", "🔥", "🗞️", "🗑️", "🤡", "👻"]


class GivenElementForm(BaseModel):
    url: AnyHttpUrl
    name: str
    tags: Set[TagList] | None = None


class TagFilterForm(BaseModel):
    tags: Set[TagList] | None = None
