import json
from datetime import datetime
from typing import List

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from pydantic import AnyHttpUrl

from pochurl.core.storage import Storage
from pochurl.domain import GivenElement, SavedElement


class FireStoreStorage(Storage):
    cred = credentials.Certificate('pochurl-firebase.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client().collection('elements')

    def read_item(self, id: str) -> SavedElement | None:
        previous = self.db.document(id).get()
        return SavedElement(id=previous.id, **previous.to_dict()) if previous.exists else None

    def read_items(self) -> List[SavedElement]:
        previous = self.db.stream()
        return [SavedElement(id=p.id, **p.to_dict()) for p in previous] if previous else []

    def read_items_by_name(self, name: str) -> List[SavedElement]:
        # https://stackoverflow.com/a/47916173
        condition = FieldFilter('name', '>=', name)
        previous = self.db.where(filter=condition).stream()
        return [SavedElement(id=p.id, **p.to_dict()) for p in previous] if previous else []

    def read_items_by_url(self, url: AnyHttpUrl) -> List[SavedElement]:
        condition = FieldFilter('url', '>=', str(url))
        previous = self.db.where(filter=condition).stream()
        return [SavedElement(**(p.to_dict() | {'id': p.id})) for p in previous] if previous else []

    def write_item(self, element: GivenElement) -> str:
        new = self.db.document()
        new.set(json.loads(element.json()) | {'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')})
        return new.id

    def rewrite_item(self, id: str, element: GivenElement) -> str | None:
        previous = self.read_item(id)
        if previous:
            new = self.db.document(id)
            timestamp = previous.timestamp if previous else datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
            new.set(json.loads(element.json()) | {'timestamp': timestamp})
            return new.id
        print(f'no id={id} yet')
        return None
