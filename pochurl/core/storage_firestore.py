import json
from datetime import datetime
from typing import List

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from pydantic import AnyHttpUrl

from pochurl.domain import GivenElement, SavedElement


cred = credentials.Certificate('pochurl-firebase.json')
firebase_admin.initialize_app(cred)
db = firestore.client().collection('elements')


def read_item(id: str) -> SavedElement | None:
    previous = db.document(id).get()
    return SavedElement(id=previous.id, **previous.to_dict()) if previous.exists else None

def read_items() -> List[SavedElement]:
    previous = db.stream()
    return [SavedElement(id=p.id, **p.to_dict()) for p in previous] if previous else []

def read_items_by_name(name: str) -> List[SavedElement]:
    # https://stackoverflow.com/a/47916173
    condition = FieldFilter('name', '>=', name)
    previous = db.where(filter=condition).stream()
    return [SavedElement(id=p.id, **p.to_dict()) for p in previous] if previous else []

def read_items_by_url(url: AnyHttpUrl) -> List[SavedElement]:
    condition = FieldFilter('url', '>=', str(url))
    previous = db.where(filter=condition).stream()
    return [SavedElement(**(p.to_dict() | {'id': p.id})) for p in previous] if previous else []

def write_item(element: GivenElement) -> str:
    new = db.document()
    new.set(json.loads(element.json()) | {'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')})
    return new.id

def rewrite_item(id: str, element: GivenElement) -> str | None:
    previous = read_item(id)
    if previous:
        new = db.document(id)
        timestamp = previous.timestamp if previous else datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
        new.set(json.loads(element.json()) | {'timestamp': timestamp})
        return new.id
    print(f'no id={id} yet')
    return None
