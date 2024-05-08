from typing import List

from fastapi import Depends, FastAPI
from pydantic import AnyHttpUrl

from pochurl.core import get_db
from pochurl.domain import GivenElement, SavedElement


app = FastAPI(
    title='Pochurl',
    description='App to save and organize links',
)


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.get('/get/element/{id}')
def get_item(id: str, db = Depends(get_db)) -> SavedElement | None:
    return db.read_item(id)


@app.get('/get/list/')
def list_items(db = Depends(get_db)) -> List[SavedElement]:
    return db.read_items()


@app.get('/get/url/')
def get_items_by_url(url: AnyHttpUrl, db = Depends(get_db)) -> List[SavedElement]:
    return db.read_items_by_url(url)


@app.get('/get/name/')
def get_items_by_name(name: str, db = Depends(get_db)) -> List[SavedElement]:
    return db.read_items_by_name(name)


@app.put('/add/')
def add_item(element: GivenElement, db = Depends(get_db)) -> str:
    return db.write_item(element)


@app.put('/update/element/{id}')
def update_item(id: str, element: GivenElement, db = Depends(get_db)) -> str | None:
    return db.rewrite_item(id, element)
