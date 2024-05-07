from typing import List

from fastapi import FastAPI
from pydantic import AnyHttpUrl

from pochurl.core import read_item_by_url, read_items, read_items_by_name, write_item
from pochurl.domain import GivenElement, SavedElement


app = FastAPI()


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.get('/url/')
def get_item_by_url(url: AnyHttpUrl) -> SavedElement:
    return read_item_by_url(url)


@app.get('/name/')
def get_items_by_name(name: str) -> List[SavedElement]:
    return read_items_by_name(name)


@app.get('/list/')
def list_items() -> List[SavedElement]:
    return read_items()


@app.put('/element/')
def update_item(element: GivenElement):
    write_item(element)
