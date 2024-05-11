from typing import List

from fastapi import Depends, APIRouter
from pydantic import AnyHttpUrl

from pochurl.core import get_db
from pochurl.domain import GivenElement, SavedElement


router = APIRouter(prefix="/api", tags=["api"])


@router.get("/element/{element_id}")
def get_item(element_id: str, db=Depends(get_db)) -> SavedElement | None:
    return db.read_item(element_id)


@router.get("/elements")
def get_items(db=Depends(get_db)) -> List[SavedElement]:
    return db.read_items()


@router.get("/elements/url")
def get_items_by_url(url: AnyHttpUrl, db=Depends(get_db)) -> List[SavedElement]:
    return db.read_items_by_url(url)


@router.get("/elements/name")
def get_items_by_name(name: str, db=Depends(get_db)) -> List[SavedElement]:
    return db.read_items_by_name(name)


@router.put("/element")
def add_item(element: GivenElement, db=Depends(get_db)) -> str:
    return db.write_item(element)


@router.put("/element/{element_id}")
def update_item(element_id: str, element: GivenElement, db=Depends(get_db)) -> str | None:
    return db.rewrite_item(element_id, element)
