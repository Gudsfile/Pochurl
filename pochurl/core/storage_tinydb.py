import json
from datetime import datetime
from typing import List

from tinydb import TinyDB, Query
from tinydb.table import Document
from pydantic import AnyHttpUrl

from pochurl.domain import GivenElement, SavedElement


db = TinyDB('pochurl-tinydb.json')


def read_item(id: str) -> SavedElement | None:
    previous = db.get(doc_id=id)
    return SavedElement(id=id, **dict(previous)) if previous else None

def read_items() -> List[SavedElement]:
    previous = db.all()
    return [SavedElement(id=str(p.doc_id), **dict(p)) for p in previous] if previous else []

def read_items_by_name(name: str) -> List[SavedElement]:
    condition = Query().name.test(_test_str_contains, name)
    previous = db.search(condition)
    return [SavedElement(id=str(p.doc_id), **dict(p)) for p in previous] if previous else []

def read_items_by_url(url: AnyHttpUrl) -> List[SavedElement]:
    condition = Query().url.test(_test_str_contains, str(url))
    previous = db.search(condition)
    return [SavedElement(id=str(p.doc_id), **dict(p)) for p in previous] if previous else []

def write_item(element: GivenElement) -> str:
    id = db.insert(json.loads(element.json()) | {'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')})
    return str(id)

def rewrite_item(id: str, element: GivenElement) -> str | None:
    previous = read_item(id)
    if previous:
        db.upsert(Document(json.loads(element.json()), doc_id = int(id)))
        return id
    print(f'no id={id} yet')
    return None

def _test_str_contains(val, string):
    return string.lower() in val.lower()
