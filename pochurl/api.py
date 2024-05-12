from textwrap import dedent
from typing import List

from fastapi import APIRouter, Depends, Request
from pydantic import AnyHttpUrl

from pochurl.core import get_db
from pochurl.domain import AddResponse, GivenElement, SavedElement
from pochurl.importer import csv_to_dicts, dict_to_elements

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


@router.put("/elements")
def add_items(elements: List[GivenElement], db=Depends(get_db)) -> AddResponse:
    return AddResponse(added_ids=[db.write_item(element) for element in elements])


@router.put("/str-elements")
def add_str_items(csv_elements: List[str], db=Depends(get_db)) -> AddResponse:
    csv_elements = "\n".join(csv_elements)
    elements, errors = dict_to_elements(csv_to_dicts(csv_elements))
    return AddResponse(added_ids=[db.write_item(element) for element in elements], errors=errors)


@router.put(
    "/csv-elements",
    openapi_extra={
        "requestBody": {
            "content": {
                "text/csv": {
                    "schema": {
                        "title": "CsvRow",
                        "type": "string",
                        "example": dedent(
                            """
                            https://example1.py,name1,tag1
                            https://example2.py,name2,"tag2,another-tag2"
                            """
                        ),
                    }
                }
            },
            "required": True,
        },
    },
)
async def add_csv_items(request: Request, db=Depends(get_db)) -> AddResponse:
    csv_elements = await request.body()
    csv_elements = csv_elements.decode("utf-8")
    elements, errors = dict_to_elements(csv_to_dicts(csv_elements))
    return AddResponse(added_ids=[db.write_item(element) for element in elements], errors=errors)
