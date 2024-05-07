import json
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from pydantic import AnyHttpUrl

from pochurl.domain import GivenElement, SavedElement


cred = credentials.Certificate('pochurl-firebase.json')
firebase_admin.initialize_app(cred)
db = firestore.client().collection('elements')


def read_items_by_url(url: AnyHttpUrl):
    previous = db.where(filter=FieldFilter('url', '>=', str(url))).stream()
    return [SavedElement(**(p.to_dict() | {'id': p.id})) for p in previous] if previous else None

def read_items_by_name(name: str):
    # https://stackoverflow.com/a/47916173
    previous = db.where(filter=FieldFilter('name', '>=', name)).stream()
    return [SavedElement(**(p.to_dict() | {'id': p.id})) for p in previous] if previous else None

def read_item(id: str):
    previous = db.document(id).get()
    return SavedElement(**(previous.to_dict() | {'id': previous.id})) if previous.exists else None

def read_items():
    previous = db.stream()
    return [SavedElement(**(p.to_dict() | {'id': p.id})) for p in previous] if previous else None

def write_item(element: GivenElement):
    new = db.document()
    new.set(json.loads(element.json()) | {'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')})
    return new.id

def rewrite_item(id: str, element: GivenElement):
    previous = read_item(id)
    if previous:
        new = db.document(id)
        timestamp = previous.timestamp if previous else datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
        new.set(json.loads(element.json()) | {'timestamp': timestamp})
        return new.id
    print(f'no id={id} yet')
    return None
