import json
from datetime import datetime

from tinydb import TinyDB, Query
from tinydb.table import Document
from pydantic import AnyHttpUrl

from pochurl.domain import GivenElement, SavedElement


db = TinyDB('pochurl-tinydb.json')


def read_item_by_url(url: AnyHttpUrl):
    Element = Query()
    condition = Element.url == str(url)
    previous = db.get(condition)
    return SavedElement(**previous) if previous else {}

def read_items_by_name(name: str):
    Element = Query()
    def test_func(val, name):
        return (name.lower() in val.lower()) if name else True
    condition = Element.name.test(test_func, name)
    previous = db.search(condition)
    return [SavedElement(**p) for p in previous] if previous else []

def read_items():
    previous = db.all()
    return [SavedElement(**p) for p in previous] if previous else []

def write_item(element: GivenElement):
    Element = Query()
    previous = db.get(Element.url == str(element.url))
    if previous:
        return db.upsert(Document(json.loads(element.json()), doc_id = previous.doc_id))
    return db.insert(json.loads(element.json()) | {'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')})
