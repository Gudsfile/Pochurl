from typing import Literal

from pydantic import AnyHttpUrl, BaseModel


TagList = Literal["👀", "✨", "🚨", "🔥", "🗞️", "🗑️", "🤡", "👻"]


class GivenElementForm(BaseModel):
    url: AnyHttpUrl
    name: str
    tag: TagList | None = None


class TagFilterForm(BaseModel):
    tag: TagList | None = None
