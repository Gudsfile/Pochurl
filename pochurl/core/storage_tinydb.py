import json
from datetime import datetime

from tinydb import TinyDB, Query
from tinydb.table import Document
from pydantic import AnyHttpUrl

from pochurl.domain import GivenElement, SavedElement


db = TinyDB('pochurl-tinydb.json')


def read_items_by_url(url: AnyHttpUrl):
    Element = Query()
    condition = Query().url.test(_test_str_contains, str(url))
    previous = db.search(condition)
    return [SavedElement(**(dict(p) | {'id': str(p.doc_id)})) for p in previous] if previous else None

def read_items_by_name(name: str):
    Element = Query()
    condition = Query().name.test(_test_str_contains, name)
    previous = db.search(condition)
    return [SavedElement(**(dict(p) | {'id': str(p.doc_id)})) for p in previous] if previous else None

def read_item(id: str):
    previous = db.get(doc_id=id)
    return SavedElement(**(dict(previous) | {'id': id})) if previous else None

def read_items():
    previous = db.all()
    print(previous)
    return [SavedElement(**(dict(p) | {'id': str(p.doc_id)})) for p in previous] if previous else None

def write_item(element: GivenElement):
    id = db.insert(json.loads(element.json()) | {'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')})
    return str(id)

def rewrite_item(id: str, element: GivenElement):
    previous = read_item(id)
    if previous:
        db.upsert(Document(json.loads(element.json()), doc_id = int(id)))
        return id
    print(f'no id={id} yet')
    return None

def _test_str_contains(val, string):
    return string.lower() in val.lower()
