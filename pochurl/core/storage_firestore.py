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


def read_item_by_url(url: AnyHttpUrl):
    previous = db.where(filter=FieldFilter('url', '==', str(url))).stream()
    return [SavedElement(**p.to_dict()) for p in previous][0] if previous else {}

def read_items_by_name(name: str):
    # https://stackoverflow.com/a/47916173
    previous = db.where(filter=FieldFilter('name', '>=', name)).stream()
    return [SavedElement(**p.to_dict()) for p in previous] if previous else []

def read_items():
    previous = db.stream()
    return [SavedElement(**p.to_dict()) for p in previous] if previous else []

def write_item(element: GivenElement):
    new = db.document()
    return new.set(json.loads(element.json()) | {'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')})
