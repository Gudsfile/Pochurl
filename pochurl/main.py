import json
from datetime import datetime
from typing import List, Set, Union

from fastapi import FastAPI
from pydantic import AnyHttpUrl, BaseModel
from tinydb import TinyDB, Query
from tinydb.table import Document


class GivenElement(BaseModel):
    url: AnyHttpUrl
    name: str
    tags: Set[str]

class SavedElement(GivenElement):
    timestamp: datetime


db = TinyDB('db.json')
app = FastAPI()


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.get('/url/')
def get_item_by_url(url: AnyHttpUrl) -> SavedElement:
    Element = Query()
    condition = Element.url == str(url)
    previous = db.get(condition)
    if previous:
        return SavedElement(**previous)
    return {}


@app.get('/name/')
def get_items_by_name(name: str) -> List[SavedElement]:
    Element = Query()
    def test_func(val, name):
        return (name.lower() in val.lower()) if name else True
    condition = Element.name.test(test_func, name)
    previous = db.search(condition)
    if previous:
        return [SavedElement(**p) for p in previous]
    return []


@app.get('/list/')
def list_items() -> List[SavedElement]:
    previous = db.all()
    if previous:
        return [SavedElement(**p) for p in previous]
    return []


@app.put('/element/')
def update_item(element: GivenElement):
    Element = Query()
    previous = db.get(Element.url == str(element.url))
    if previous:
        return db.upsert(Document(json.loads(element.json()), doc_id = previous.doc_id))
    return db.insert(json.loads(element.json()) | {'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')})
