from typing import List

from fastapi import FastAPI
from pydantic import AnyHttpUrl

from pochurl.core import read_item, read_items, read_items_by_name, read_items_by_url, rewrite_item, write_item
from pochurl.domain import GivenElement, SavedElement


app = FastAPI()


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.get('/get/url/')
def get_items_by_url(url: AnyHttpUrl) -> List[SavedElement]:
    return read_items_by_url(url)


@app.get('/get/name/')
def get_items_by_name(name: str) -> List[SavedElement]:
    return read_items_by_name(name)


@app.get('/get/list/')
def list_items() -> List[SavedElement]:
    return read_items()


@app.get('/get/element/{id}')
def get_item(id: str) -> SavedElement:
    return read_item(id)


@app.put('/add/')
def add_item(element: GivenElement) -> str:
    return write_item(element)


@app.put('/update/element/{id}')
def update_item(id: str, element: GivenElement) -> str | None:
    return rewrite_item(id, element)
